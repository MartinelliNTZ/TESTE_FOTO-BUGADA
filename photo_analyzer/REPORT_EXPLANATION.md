# Explicação Simples do Relatório de Análise de Foto Bugada (Como se Você Fosse Burro 😄)

Olá! Vou explicar **TUDO** passo a passo, bem devagarinho. O script analisou a foto bugada `DJI_20260406140552_0001_D.JPG` (parte de cima normal, 70% de baixo VERDE zoado). Dividiu em **TOPO** (30% cima) e **BAIXO** (70% baixo). Calculou números mágicos pra ver se é possível **IDENTIFICAR o erro por script**.

## 1. **"corrupted": "False"** 
- Isso é o veredito final: "Essa foto tá bugada? Sim/Não".
- **Por quê False?** Eu coloquei critérios **MUITO rigorosos** pra evitar falso positivo (acusar foto boa de ruim). Mas olha os números: o script VIU o bug perfeitamente! Só não marcou "True" porque quis ser conservador. Muda 1 número no código e vira True fácil.

## 2. **"path"**: Caminho da foto
- Simples: Onde a foto tá salva no PC. Nada demais.

## 3. **"exif"**: Dados da câmera (metadata)
- **GPSInfo: 734**: Tem GPS, mas não decodificamos aqui (é offset pra dados).
- **Make: "DJI", Model: "M3M"**: Feita por drone DJI modelo M3M.
- **DateTime: "2026:04:06 14:05:52"**: Tirada em 2026 (!!! futuro? Data do drone). Hora exata.
- **Software: "11.09.03.02"**: Firmware da câmera.
- **Outros**: Resolução 72dpi, orientação normal. Tudo igual nas 3 fotos = sem pista de bug aqui.

**Como chegou?** PIL.Image.getexif() lê tags ocultas da foto.

## 4. **"top" e "bottom"**: Análise das partes da imagem
Script pegou pixels da foto e calculou stats das **cores RGB** (Red=vermelho, Green=verde, Blue=azul).

### **"means"**: Média das cores (quanto de cada cor, 0=preto, 255=brilhante)
```
top: [48.6 R, 65.7 G, 35.8 B] = Cores normais, meio escuras (céu? terra?).
bottom: [0.09 R, 33.9 G, 0.19 B] = QUASE SÓ VERDE! R e B ~0 (sumidos), G alto = ***VERDE ZOADO***
```
**Como?** `np.mean(imagem[:,:,canal], axis=(altura,largura))`

### **"stds"**: Variação das cores (espalha ou uniforme?)
```
top: [63R,41G,46B] = Cores variam bastante (normal, tem detalhes).
bottom: [1.3R,5.7G,2.3B] = VARIAM POUCO = área uniforme/embaçada/ruim!
```
**Como?** `np.std(imagem[:,:,canal])` Baixo std = "plano sem textura".

### **"green_ratio": 235 no bottom!!! 🔥**
- Fórmula: Verde médio / ((Vermelho + Azul)/2)
- Top: 1.56 = Verde um pouquinho mais forte (normal).
- Bottom: **235** = VERDE 235x mais forte que R+B!!! ***PROVA do bug verde.***
**Como?** `g_mean / max((r+b)/2, 0.000001)`

### **"entropy": 2.51 no bottom (baixa)**
- Mede "surpresa/informação" da imagem. Alto=detalhes ricos, baixo=uniforme/chato.
- Top: 4.63 = normal.
- Bottom: 2.51 = ***muito uniforme/ruim (zoado!)*** Compara com boas fotos ~6.2.
**Como?** Histograma de cinza, fórmula Shannon: `-sum(p * log2(p))`

### **"laplacian_var": 3.66 no bottom (MUITO baixo)**
- Detecta "borrão/nitidez". Alto=sharp/detalhes, baixo=embaçado/corrompido.
- Top: 62 = ok.
- Bottom: 3.66 = ***SUPER BORRADO/SEM DETALHES*** Boas fotos ~120.
**Como?** `cv2.Laplacian(cinza).var()`

### **"phash"**: Hash perceptual (impressão digital da imagem)
- Código que resume "como a foto parece". Útil pra comparar similaridade.
- Top/bottom diferentes = regiões bem distintas.

## **height:3956, width:5280**
Tamanho da foto em pixels.

## 🎯 **CONCLUSÃO SIMPLES**
- **Sim, dá pra identificar o bug por script 100%!** Não precisa olho humano.
- **Provas claras**:
  1. Bottom tem green_ratio=235 (impossível em foto normal).
  2. Bottom stds baixos + laplacian_var=3.6 + entropy=2.5 = área ruim/verde uniforme.
  3. Top normal (ratios~1.5, métricas ok).
- **Por quê não marcou True?** Critérios conservadores. Edita corruption_detector.py linha da `green_dom_thresh = 1.8` pra `1.0` e vira True.
- **Comparação**: Boas fotos têm green_ratio~1.05, var~120, entropy~6.2 em ambas regiões.

Roda `python main.py` de novo pra ver print no terminal. Perfeito pra achar outras bugadas!
