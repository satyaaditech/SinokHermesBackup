---
name: ai-trading-bot
title: AI Trading Bot Architecture
description: Build algorithmic trading bots with multi-layer architecture, AI signal aggregation, and risk management
tags: [trading, algorithmic, alpaca, crypto, forex, bot]
---

# AI Trading Bot Development

## Overview

Build automated trading bots using a 3-layer architecture pattern that separates data ingestion, AI decision-making, and execution. Optimized for Alpaca Markets API but adaptable to other brokers.

## Architecture Pattern

```
LAYER 3: AI Decision Engine
→ Signal aggregation & scoring
→ Entry/exit logic

LAYER 2: Technical Analysis
→ Indicators (EMA, RSI, MACD, BB)
→ Pattern detection

LAYER 1: Data & Execution
→ Market data fetching
→ Order management
```

## Project Structure

```
trading-bot/
├── main.py                    # Entry point
├── config.yaml                # Strategy parameters
├── data/broker_client.py      # API wrapper
├── indicators/technical.py    # TA calculations
├── ai/signal_aggregator.py   # Signal combination
├── strategies/strategy.py    # Entry/exit rules
├── risk/manager.py           # Risk management
├── execution/order_manager.py # Order execution
└── backtest/backtester.py    # Historical testing
```

## Key Components

### 1. Technical Indicators

```python
class TechnicalIndicators:
    def calculate_all(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.add_ema(df)        # Trend
        df = self.add_rsi(df)        # Momentum
        df = self.add_macd(df)       # Crossover
        df = self.add_bollinger(df)  # Volatility
        df = self.add_atr(df)        # Risk sizing
        return df
```

### 2. AI Signal Aggregator

```python
class SignalAggregator:
    def __init__(self, config):
        self.weights = {
            'ema_cross': 0.25,
            'macd_signal': 0.25,
            'bollinger_bounce': 0.20,
            'rsi_divergence': 0.20,
            'volume_spike': 0.10
        }
    
    def calculate_signal_strength(self, scores, data) -> Tuple[float, str]:
        bullish = sum(scores[k] * self.weights[k] for k in scores if scores[k] > 0)
        bearish = sum(abs(scores[k]) * self.weights[k] for k in scores if scores[k] < 0)
        
        if bullish > bearish:
            return bullish, "BUY"
        elif bearish > bullish:
            return bearish, "SELL"
        return 0.5, "NEUTRAL"
```

### 3. Risk Management

**Position Sizing:**
```
Position Size = (Account × Risk%) / (|Entry - Stop Loss|)
```

**Key Limits:**
- Max 2% risk per trade
- Max 6% daily loss → stop trading
- Max 3 consecutive losses → cooldown
- Max 3 open positions

### 4. Trading Loop

```python
def trading_iteration(self):
    # Update positions
    self.update_positions()
    
    # Risk checks
    if not self.risk_manager.check_trade_allowed(equity, len(positions)):
        return
    
    # Check exits
    for symbol in positions:
        if self.should_exit(position, current_data):
            self.close_position(symbol)
    
    # Scan for entries
    opportunities = self.scan_market(symbols)
    for opp in opportunities:
        if opp['confidence'] > threshold:
            size = self.calculate_position_size(...)
            self.enter_position(opp, size)
```

## Configuration Template

```yaml
broker:
  paper: true  # Start with paper trading!

trading:
  timeframe: "5Min"
  max_positions: 3

indicators:
  ema: {fast: 9, slow: 21}
  rsi: {period: 14, oversold: 30, overbought: 70}

ai_weights:
  ema_cross: 0.25
  macd_signal: 0.25
  bollinger_bounce: 0.20

risk:
  risk_per_trade: 0.02      # 2%
  max_daily_loss: 0.06      # 6%
  reward_ratio: 1.5         # 1:1.5
  stop_loss_atr: 2.0        # 2x ATR
```

## Entry/Exit Rules

### Entry:
1. AI confidence > 65%
2. Volatility > minimum
3. Within risk limits
4. No correlation conflict

### Exit:
1. Stop loss hit (2x ATR)
2. Take profit hit (1.5x risk)
3. Signal drops below 40%
4. Direction reversal
5. Max hold time exceeded

## Safety Rules

⚠️ CRITICAL:
1. Always start with paper trading
2. Backtest 30+ days before live
3. Set max daily loss limits
4. Use proper position sizing
5. Log everything
6. Test emergency stop

## Common Pitfalls

| Mistake | Solution |
|---------|----------|
| Over-optimizing | Walk-forward analysis |
| Ignoring slippage | Add 0.1% in backtest |
| Curve fitting | Simpler rules |
| No risk limits | Hard stops |
| Emotional trading | Full automation |

## References

- Alpaca API: https://alpaca.markets/docs/
- TA-Lib: https://github.com/TA-Lib/ta-lib-python