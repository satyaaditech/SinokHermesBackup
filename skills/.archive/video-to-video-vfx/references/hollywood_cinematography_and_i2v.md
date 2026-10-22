# Hollywood Cinematography & Image-to-Video (I2V) Motion Prompts

Reference guide for 2-stage generative video (Gemini Imagen 3 Keyframe -> Google Veo / Flow / Runway / Kling Motion).

## 1. Camera Movement Directives
- **Vertigo Effect / Dolly Zoom**: `Dramatic Vertigo effect (dolly zoom), camera rapidly pushes in while background field of view widens, subject locked in center, disorienting spatial warp.`
- **Dutch Angle / Canted**: `Dutch angle shot, tilted camera perspective, dramatic slanted composition, intense unsettling mood.`
- **Ascending Crane**: `Ascending crane shot, camera lifts smoothly from ground level revealing vast majestic landscape above, 24fps steady motion.`
- **360 Orbit**: `Slow 360-degree orbital camera revolution around subject, maintaining steady subject lock, fluid background rotation.`
- **Tracking Follow**: `Smooth cinematic tracking shot following subject forward at steady pace, fluid motion blur on passing environment.`

## 2. Cinematic Lighting Lexicon
- **Rembrandt Lighting**: `Rembrandt lighting style, distinct triangle of light on shaded cheek, high key-to-fill contrast, moody studio portrait.`
- **Chiaroscuro**: `Dramatic chiaroscuro lighting, deep rich shadow gradients, intense single light source, Caravaggio aesthetic.`
- **Golden Hour**: `Golden hour warm honey lighting, soft glowing sun flare, long ambient shadows, romantic warmth.`
- **Volumetric Rim Light**: `Strong volumetric rim lighting, radiant edge light separating silhouette from dark atmospheric background.`

## 3. The 2-Stage Keyframe Pipeline
1. **Stage 1 (Keyframe)**: `[Shot Type & Angle] + [Subject & Pose] + [Environment] + [Lighting & Color] + [Lens Optics]`
2. **Stage 2 (Motion Prompt)**: `[Camera Vector & Speed] + [Dynamic Subject Action] + [Environmental Physics/Particles] + [Stability]`
