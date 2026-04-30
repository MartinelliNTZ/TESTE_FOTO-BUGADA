# Cores para Análise de Fotos - Guia Simples

## 1. RGB (já funcionando) ✅
- Vermelho, Verde, Azul (os 3 canais básicos)
- Detecta: dominante, desbalanceamento, ratios
- Bom para detectar fotos ruins básicas

## 2. HSV (melhor para fotos reais) 🔥 **RECOMENDADO**
- **Hue** (cor dominante): céu azul vs verde planta
- **Saturation** (intensidade cor): foto lavada ou vibrante  
- **Value** (brilho): sub/ sobreexposta
- **Por que usar**: HSV é como olho humano vê cores

## 3. LAB (cores profissionais) 👍
- **L** (clareza): claro/escuro
- **a** (vermelho x verde)
- **b** (amarelo x azul)
- **Por que usar**: Detecta cores estranhas em drone

## 4. Grayscale (preto e branco) ⚪
- **Intensidade média**: foto clara/escura geral
- **Variação**: contraste
- **Por que usar**: simples, rápido, bom para textura

## 5. YUV (para JPEG ruins) 📱
- **Y** (brilho)
- **U/V** (cores)
- **Por que usar**: detecta corrupção JPEG drone

## Qual usar agora?
1. **HSV** (mais fácil e útil)
2. **LAB** (profissional)
3. **Grayscale** (simples)

**Diga**: "HSV primeiro" ou "LAB e HSV"

**Teste atual**: RGB já roda perfeito no Excel/JSON.
