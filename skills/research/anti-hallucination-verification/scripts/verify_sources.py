#!/usr/bin/env python3
"""
verify_sources.py - Fact-Checking Module for YouTube Automation Pipeline
=========================================================================

Purpose: Verify all claims and data against official sources to prevent hallucination.

What it does:
1. Parse URLs from research results
2. Fetch and save HTML from each source
3. Extract claims from transcript/content
4. Cross-check claims against source content
5. Flag/remove unverifiable claims
6. Output: Verified data points only

Usage:
    python3 verify_sources.py --sources sources.json --transcript transcript.txt --output verified_data.json

Author: Sinok (Hermes Agent)
Created: 2026-05-01
"""

import argparse
import json
import re
import os
import sys
from datetime import datetime
from urllib.parse import urlparse
import subprocess


class SourceVerifier:
    """Verify claims against official sources to prevent hallucination."""
    
    # Trusted domains (add more as needed)
    TRUSTED_DOMAINS = [
        'openai.com',
        'google.com',
        'anthropic.com',
        'meta.com',
        'microsoft.com',
        'github.com',
        'wikipedia.org',
        'techcrunch.com',
        'theverge.com',
        'arstechnica.com',
        'wired.com',
        'reuters.com',
        'bloomberg.com',
        'cnbc.com',
        'youtube.com',  # Official channels only
    ]
    
    # Untrusted domains to block
    BLOCKED_DOMAINS = [
        'medium.com',  # Can be anyone
        'reddit.com',
        'quora.com',
        'tiktok.com',
        'facebook.com',
        'twitter.com',  # Use with caution
    ]
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.verified_claims = []
        self.unverified_claims = []
        self.blocked_sources = []
        self.fetch_errors = []
        
    def log(self, message, level="INFO"):
        """Print log message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] [{level}] {message}")
    
    def is_trusted_domain(self, url):
        """Check if URL is from a trusted domain."""
        try:
            domain = urlparse(url).netloc.lower()
            # Remove www. prefix
            domain = domain.replace('www.', '')
            
            # Check blocked domains first
            for blocked in self.BLOCKED_DOMAINS:
                if blocked in domain:
                    return False, f"Blocked domain: {blocked}"
            
            # Check trusted domains
            for trusted in self.TRUSTED_DOMAINS:
                if trusted in domain:
                    return True, f"Trusted domain: {trusted}"
            
            # Unknown domain - flag for manual review
            return None, f"Unknown domain: {domain} (needs manual review)"
            
        except Exception as e:
            return False, f"Error parsing URL: {str(e)}"
    
    def fetch_source(self, url, output_dir='/tmp/source_verification'):
        """
        Fetch HTML from URL and save for verification.
        Returns: (success, file_path, content_snippet)
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename from URL
        safe_name = re.sub(r'[^\w\-_]', '_', urlparse(url).path)[:50]
        filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(output_dir, filename)
        
        try:
            self.log(f"Fetching: {url}")
            
            # Use curl to fetch (safer than requests for verification)
            cmd = [
                'curl', '-sL',
                '--max-time', '10',  # 10 second timeout
                '--user-agent', 'Mozilla/5.0 (compatible; SourceVerifier/1.0)',
                '-o', filepath,
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode != 0:
                self.log(f"Failed to fetch {url}: {result.stderr}", "ERROR")
                self.fetch_errors.append({
                    'url': url,
                    'error': result.stderr,
                    'timestamp': datetime.now().isoformat()
                })
                return False, None, None
            
            # Read and extract text content (basic HTML stripping)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()
            
            # Strip HTML tags for text extraction
            text_content = re.sub(r'<[^>]+>', ' ', html_content)
            text_content = re.sub(r'\s+', ' ', text_content).strip()
            
            self.log(f"Successfully fetched: {url} ({len(text_content)} chars)")
            return True, filepath, text_content[:5000]  # First 5000 chars for verification
            
        except subprocess.TimeoutExpired:
            self.log(f"Timeout fetching {url}", "ERROR")
            self.fetch_errors.append({
                'url': url,
                'error': 'Timeout after 15 seconds',
                'timestamp': datetime.now().isoformat()
            })
            return False, None, None
            
        except Exception as e:
            self.log(f"Error fetching {url}: {str(e)}", "ERROR")
            self.fetch_errors.append({
                'url': url,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return False, None, None
    
    def extract_claims(self, transcript_text):
        """
        Extract factual claims from transcript text.
        Looks for: numbers, dates, benchmarks, statistics, specific assertions.
        
        Returns: List of claim dictionaries
        """
        claims = []
        
        # Pattern 1: Numbers with context (benchmarks, scores, etc.)
        number_pattern = r'(\d+(?:\.\d+)?(?:%|M|B|K)?)\s*(?:on|in|at|for|of|scored|reached|achieved)\s+([A-Za-z][\w\s]{5,50})'
        for match in re.finditer(number_pattern, transcript_text, re.IGNORECASE):
            claims.append({
                'type': 'numerical',
                'text': match.group(0),
                'value': match.group(1),
                'context': match.group(2),
                'verified': False,
                'source': None
            })
        
        # Pattern 2: Product/model announcements
        product_pattern = r'((?:GPT|Claude|Gemini|Llama|AI|Model)\s*[-\d\.]*)\s*(?:released|launched|announced|introduced|updated)'
        for match in re.finditer(product_pattern, transcript_text, re.IGNORECASE):
            claims.append({
                'type': 'product_announcement',
                'text': match.group(0),
                'product': match.group(1),
                'verified': False,
                'source': None
            })
        
        # Pattern 3: Date/time claims
        date_pattern = r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|\d{1,2}/\d{1,2}/\d{4})'
        for match in re.finditer(date_pattern, transcript_text, re.IGNORECASE):
            claims.append({
                'type': 'date',
                'text': match.group(1),
                'date': match.group(1),
                'verified': False,
                'source': None
            })
        
        # Pattern 4: Comparative claims (faster, better, etc.)
        comparative_pattern = r'((?:\d+x|\d+ times|significantly|substantially)\s*(?:faster|better|slower|larger|smaller))'
        for match in re.finditer(comparative_pattern, transcript_text, re.IGNORECASE):
            claims.append({
                'type': 'comparative',
                'text': match.group(1),
                'comparison': match.group(1),
                'verified': False,
                'source': None
            })
        
        self.log(f"Extracted {len(claims)} claims from transcript")
        return claims
    
    def verify_claim(self, claim, source_content):
        """
        Verify a single claim against source content.
        Returns: (is_verified, confidence_score, evidence)
        """
        claim_text = claim.get('text', '').lower()
        claim_value = claim.get('value', claim.get('product', claim.get('date', ''))).lower()
        
        if not source_content:
            return False, 0, "No source content available"
        
        source_lower = source_content.lower()
        
        # Check if claim value appears in source
        if claim_value and claim_value in source_lower:
            # Extract surrounding context for evidence
            idx = source_lower.find(claim_value)
            start = max(0, idx - 100)
            end = min(len(source_lower), idx + 200)
            evidence = source_lower[start:end]
            
            return True, 0.9, f"Found in source: ...{evidence}..."
        
        # Check for partial matches (numbers, key terms)
        numbers_in_claim = re.findall(r'\d+(?:\.\d+)?', claim_text)
        if numbers_in_claim:
            matches = 0
            for num in numbers_in_claim:
                if num in source_lower:
                    matches += 1
            
            if matches > 0:
                confidence = matches / len(numbers_in_claim)
                if confidence >= 0.5:
                    return True, confidence, f"Partial match: {matches}/{len(numbers_in_claim)} numbers found"
        
        return False, 0, "Claim not found in source content"
    
    def verify_all(self, sources_file, transcript_file, output_file):
        """
        Main verification workflow.
        
        Args:
            sources_file: JSON file with list of source URLs
            transcript_file: Text file with transcript/content to verify
            output_file: JSON file to write verified results
        """
        self.log("=" * 60)
        self.log("STARTING SOURCE VERIFICATION")
        self.log("=" * 60)
        
        # Load sources
        try:
            with open(sources_file, 'r') as f:
                sources = json.load(f)
            self.log(f"Loaded {len(sources)} sources from {sources_file}")
        except Exception as e:
            self.log(f"Error loading sources: {e}", "ERROR")
            sources = []
        
        # Load transcript
        try:
            with open(transcript_file, 'r') as f:
                transcript_text = f.read()
            self.log(f"Loaded transcript ({len(transcript_text)} chars) from {transcript_file}")
        except Exception as e:
            self.log(f"Error loading transcript: {e}", "ERROR")
            transcript_text = ""
        
        # Step 1: Verify source domains
        self.log("\n" + "=" * 40)
        self.log("STEP 1: VERIFYING SOURCE DOMAINS")
        self.log("=" * 40)
        
        verified_sources = []
        for source in sources:
            url = source.get('url', source) if isinstance(source, dict) else source
            is_trusted, message = self.is_trusted_domain(url)
            
            if is_trusted is True:
                self.log(f"✓ TRUSTED: {url} - {message}")
                verified_sources.append(url)
            elif is_trusted is None:
                self.log(f"⚠ UNKNOWN: {url} - {message} (flagged for review)", "WARNING")
                # Still include but flag
                verified_sources.append(url)
            else:
                self.log(f"✗ BLOCKED: {url} - {message}", "ERROR")
                self.blocked_sources.append({
                    'url': url,
                    'reason': message
                })
        
        self.log(f"\nTrusted sources: {len(verified_sources)}/{len(sources)}")
        
        # Step 2: Fetch source content
        self.log("\n" + "=" * 40)
        self.log("STEP 2: FETCHING SOURCE CONTENT")
        self.log("=" * 40)
        
        source_contents = {}
        for url in verified_sources:
            success, filepath, content = self.fetch_source(url)
            if success:
                source_contents[url] = {
                    'filepath': filepath,
                    'content': content
                }
        
        self.log(f"Successfully fetched: {len(source_contents)}/{len(verified_sources)} sources")
        
        # Step 3: Extract claims from transcript
        self.log("\n" + "=" * 40)
        self.log("STEP 3: EXTRACTING CLAIMS")
        self.log("=" * 40)
        
        claims = self.extract_claims(transcript_text)
        
        # Step 4: Verify each claim
        self.log("\n" + "=" * 40)
        self.log("STEP 4: VERIFYING CLAIMS")
        self.log("=" * 40)
        
        for claim in claims:
            # Try to verify against each source
            best_confidence = 0
            best_evidence = None
            best_source = None
            
            for url, source_data in source_contents.items():
                is_verified, confidence, evidence = self.verify_claim(claim, source_data['content'])
                
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_evidence = evidence
                    best_source = url
            
            # Mark claim as verified if confidence >= 0.7
            if best_confidence >= 0.7:
                claim['verified'] = True
                claim['confidence'] = best_confidence
                claim['evidence'] = best_evidence
                claim['source'] = best_source
                self.verified_claims.append(claim)
                self.log(f"✓ VERIFIED ({best_confidence:.1%}): {claim['text'][:50]}...")
            else:
                claim['verified'] = False
                claim['confidence'] = best_confidence
                claim['reason'] = best_evidence or "Low confidence match"
                self.unverified_claims.append(claim)
                self.log(f"✗ UNVERIFIED ({best_confidence:.1%}): {claim['text'][:50]}...", "WARNING")
        
        # Step 5: Generate report
        self.log("\n" + "=" * 40)
        self.log("STEP 5: GENERATING REPORT")
        self.log("=" * 40)
        
        report = {
            'verification_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_sources': len(sources),
                'trusted_sources': len(verified_sources),
                'blocked_sources': len(self.blocked_sources),
                'sources_fetched': len(source_contents),
                'total_claims': len(claims),
                'verified_claims': len(self.verified_claims),
                'unverified_claims': len(self.unverified_claims),
                'verification_rate': f"{len(self.verified_claims)/len(claims)*100:.1f}%" if claims else "N/A"
            },
            'verified_claims': self.verified_claims,
            'unverified_claims': self.unverified_claims,
            'blocked_sources': self.blocked_sources,
            'fetch_errors': self.fetch_errors,
            'source_contents': {
                url: {'filepath': data['filepath']}
                for url, data in source_contents.items()
            }
        }
        
        # Write output
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"\n✅ Verification complete!")
        self.log(f"📊 Verified: {len(self.verified_claims)}/{len(claims)} claims ({report['summary']['verification_rate']})")
        self.log(f"📁 Report saved to: {output_file}")
        
        # Print summary table
        self.log("\n" + "=" * 60)
        self.log("VERIFICATION SUMMARY")
        self.log("=" * 60)
        self.log(f"▸ Total sources checked: {len(sources)}")
        self.log(f"▸ Trusted sources: {len(verified_sources)}")
        self.log(f"▸ Blocked sources: {len(self.blocked_sources)}")
        self.log(f"▸ Claims extracted: {len(claims)}")
        self.log(f"▸ Claims verified: {len(self.verified_claims)} ✓")
        self.log(f"▸ Claims unverified: {len(self.unverified_claims)} ✗")
        self.log(f"▸ Verification rate: {report['summary']['verification_rate']}")
        
        if self.unverified_claims:
            self.log("\n⚠️  WARNING: Unverified claims detected!", "WARNING")
            self.log("These claims should be removed or manually verified:")
            for claim in self.unverified_claims[:5]:  # Show first 5
                self.log(f"  - {claim['text'][:80]}...")
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Verify claims against official sources to prevent hallucination'
    )
    parser.add_argument(
        '--sources', '-s',
        required=True,
        help='JSON file with list of source URLs'
    )
    parser.add_argument(
        '--transcript', '-t',
        required=True,
        help='Text file with transcript/content to verify'
    )
    parser.add_argument(
        '--output', '-o',
        default='verified_data.json',
        help='Output JSON file for verification results (default: verified_data.json)'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress verbose output'
    )
    
    args = parser.parse_args()
    
    verifier = SourceVerifier(verbose=not args.quiet)
    report = verifier.verify_all(args.sources, args.transcript, args.output)
    
    # Exit with error code if verification rate is too low
    verification_rate = float(report['summary']['verification_rate'].rstrip('%')) if report['summary']['verification_rate'] != 'N/A' else 0
    
    if verification_rate < 50:
        print(f"\n❌ CRITICAL: Verification rate too low ({verification_rate}%)")
        print("Review unverified claims before proceeding!")
        sys.exit(1)
    elif verification_rate < 80:
        print(f"\n⚠️  WARNING: Verification rate is {verification_rate}%")
        print("Some claims could not be verified.")
        sys.exit(0)
    else:
        print(f"\n✅ SUCCESS: Verification rate is {verification_rate}%")
        sys.exit(0)


if __name__ == '__main__':
    main()
