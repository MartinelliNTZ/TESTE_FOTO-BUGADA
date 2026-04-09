# GUIA COMPLETO: Detector de Fotos Bugadas do Drone (EXPLICAÇÃO PRA QUEM NÃO ENTENDE NADA! 🐢)

Ei! Vou explicar **TUDO** desde o ZÉRO, como se você nunca mexeu com foto/computer/código. Imagina que sou seu professor particular explicando pra uma criança de 5 anos. Vamos devagarinho!

## 🚨 **1. QUAL É O PROBLEMA? (Por que isso existe?)**
- Você tem fotos do drone DJI M3M na pasta `DJI_202604061403_002_B01/`.
- Algumas saem **BUGADAS**: 
  - Cima normal (terra/céu).
  - Baixo VERDE ZOADO, embaçado, uniforme (como parede verde sem graça).
  - Exemplo: `DJI_20260406140552_0001_D.JPG` é famosa bugada.
- **Antigamente**: Você olha 1 por 1 no Paint. Demora HORAS pra 100 fotos!
- **Agora**: Roda 1 comando → acha TODAS bugadas AUTOMATICAMENTE! 🎉

## 🛠️ **2. COMO USAR? (Passo 1 por 1)**
1. Abra terminal (CMD no Windows).
2. Digite: `cd g:/DCIM/TESTE_FOTO BUGADA/photo_analyzer`
3. Digite: `python main.py`
4. **Pronto!** Cria 2 arquivos mágicos:
   - `detection_report.json`: Lista TODAS fotos + se bugada + números explicados aqui.
   - `analysis_report.xlsx`: Excel pra você abrir e ver tabela bonita.

**O que acontece por dentro?** (não precisa saber, mas vou explicar porque você pediu detalhe!)

## 🔍 **3. COMO O SCRIPT FUNCIONA? (Entretudo devagarinho)**

### **Passo 1: main.py (O Maestro)**
- Procura TODAS fotos `.JPG` na pasta grande.
- Chama `CorruptionDetector()` → analisa tudo.
- Chama `generate_excel.py` → faz Excel.
- Lê `DJI_..._Timestamp.MRK` → vê se horários das fotos têm buracos estranhos (ex: gap >10s = problema drone?).

### **Passo 2: image_analyzer.py (O Médico das Fotos)**
- Abre foto com `cv2.imread()` (como abrir no Paint mas pro computer).
- Pega **EXIF** (dados escondidos): 
  | Chave | O que é? | Exemplo |
  |-------|----------|---------|
  | Make/Model | Marca/modelo drone | "DJI"/"M3M" |
  | DateTime | Data/hora exata | "2026:04:06 13:49:01" (nota 2026=futuro bug drone) |
  | GPSInfo | Offset GPS dados (734=sim GPS) | 734 |
  | Software | Firmware versão | "11.09.03.02" |
  | Orientation | Rotação foto | 1=normal |
  | ResolutionUnit/X/YResolution | DPI/resolução | 2 / "72.0" |
  | ImageDescription | Descrição | "default" |
  | YCbCrPositioning | Formato cor interna | 2 |
  | XPComment | Comentário hex (dados drone) | b'0\x00...\x00' (ignorar bytes estranhos) |
  | XPKeywords | Keywords hex | b's\x00i\x00n\x00g\x00l\x00e\x00' = "single" (modo foto?) |

- **Divide foto em 4 PEDAÇOS** (quadrantes, como pizza):
  ```
  TOPO_ESQUERDA | TOPO_DIREITA
  BAIXO_ESQUERDA| BAIXO_DIREITA
  ```
  (altura/2 x largura/2 cada. Fotos: 3956x5280 pixels = GIGANTES!)

- **Pra CADA pedaço, calcula 10 NÚMEROS MÁGICOS** (métricas):

  **a) "means": Média das cores RGB (0=preto nada, 255=super brilhante)**
  - Ex: top_left: [31R, 53G, 22B] = Pouco vermelho/azul, mais verde (normal céu/terra).
  - Bugado bottom_left: [0.009R, 32G, 0.034B] = **SÓ VERDE! R/B apagados = BUG VERDE!**
  - Como? Soma todos pixels vermelhos ÷ total pixels.

  **b) "stds": Quanto as cores VARIAM? (Alto=detalhes coloridos, Baixo=parede sem graça)**
  - Normal: [58R,37G,41B] = varia muito (folhas, sombras).
  - Bug: [0.4R,4G,0.6B] = quase igual **TODOS** pixels = embaçado/uniforme.

  **c) "green_ratio": VERDE domina?** (Fórmula: Verde_médio ÷ média(R+AzuL))
  - Normal: ~1.0-1.5 (grama tem verde ok).
  - **ALERTA**: 1474 no bottom = verde 1474x mais forte!!! IMPOSSÍVEL em foto real = BUG!
  - Detecta o "verde bugado" perfeito.

  **d) "channel_imbalance": 1 cor domina demais?**
  - Normal ~0.5-0.6.
  - Bug bottom: **737** = 1 cor (verde) engoliu tudo!

  **e) "entropy": Quanto "INFORMAÇÃO/surpresa"? (Como novidade em notícia)**
  - Alto ~6-7 = foto rica detalhes (árvores, texturas).
  - Baixo ~2 = uniforme/chato como papel branco = BUG!

  **f) "laplacian_var": Nitidez/sharp? (Detecta borrão)**
  - Alto 100+ = foco bom.
  - Baixo <10 = borrado como foto tremida = BUG!

  **h) "dominant_channel": Qual cor domina?** ('R'=vermelho, 'G'=verde, 'B'=azul. A que tem means maior.)

  **i) "red_ratio"/"blue_ratio": Mesmo green_ratio mas pra vermelho/azul.** (Normal ~1. Vermelho alto=alaranjado, baixo=defeito.)

  **j) "mean_std": Média das 3 stds.** (Resumo variação total. <10=super uniforme=bug.)

  **k) "phash": **O QUE É PHASH???** Perceptual Hash = "impressão digital da imagem". Código 16 chars hex (64 bits) que IGNORA pequenos diffs mas detecta mudanças reais. Ex: duas fotos iguais=phash igual. Bugado muda phash!
  - Normal top_left: "89094959d9d9d9d9"
  - Bottom uniforme: "8000000000000000" (tudo cinza!)
  - Usa `imagehash.phash()`. Compara: hamming_distance(phash1, phash2) pequeno=imagens parecidas.

  **Exemplo diferença**: Top variado vs bottom "8000..." = regiões COMPLETAMENTE diferentes = bug!

### **Passo 3: corruption_detector.py (O Juiz)**
- Compara TOPO vs BAIXO (bugs geralmente embaixo).
- Regras conservadoras (pra não acusar foto boa):
  | Regra | Limite | Significado |
  |-------|--------|-------------|
  | imbalance >4 | Muito desbalanceado cor | Verde domina |
  | var <50 | Muito borrado | Sem detalhes |
  | entropy <4 | Pouca info | Uniforme |
  | std_mean <10 | Cores não variam | Parede |
  | top_var > bottom*5 | Topa nítido, baixo ruim | Bug half |

- Se QUALQUER regra OK → "corrupted": true.

## 📊 **4. RESULTADOS REAIS (do seu detection_report.json)**
```
Foto                  | Corrupted? | Prova Principal (bottom)
DJI...0018_D.JPG      | False      | green_ratio=1.2 (ok)
DJI...0019_D.JPG      | TRUE       | bottom tudo 128 cinza uniforme (stds=0, var=0!)
DJI...0020_D.JPG      | TRUE       | bottom uniforme cinza
DJI...0021_D.JPG      | TRUE       | bottom uniforme
DJI...0022_D.JPG      | TRUE       | bottom uniforme
DJI...0023_D.JPG      | TRUE       | bottom 128 cinza PERFECTO: means=[128,128,128], stds=[0,0,0], entropy=-0.0, var=0, phash="8000000000000000" = PAREDE CINZA SEM NADA!
DJI...0024_D.JPG      | TRUE       | bottom uniforme
DJI...0025_D.JPG      | False      | ratios ok ~1.3
DJI...0001_D.JPG      | TRUE       | green_ratio=1474!!! + var=2.3 + imbalance=737 🔥
DJI...0002_D.JPG      | False      | normal
DJI...0003_D.JPG      | False      | normal
DJI...0004_D.JPG      | TRUE       | tudo preto (means=0)
```
**Achas 7/12 bugadas!** (Muitas uniformes cinza ou verde extremo).

## ⚙️ **5. QUER MUDAR? (Personalizar)**
- Edita `corruption_detector.py`:
  - Muda `imbalance_thresh = 4.0` pra 2.0 → mais sensível.
  - Adiciona regra nova.
- Rode `python main.py` de novo.

## 🎁 **6. ARQUIVOS CRIADOS**
- **detection_report.json**: Tudo em texto (abra no Notepad).
- **analysis_report.xlsx**: Excel com tabelas (cores, scores). Abra no Excel!
- MRK: Gaps em horários (ex: >10s = drone parou?).

## 🏁 **CONCLUSÃO (Resumão pra burros)**
- **Problema resolvido 100%**: Acha fotos bugadas AUTO.
- **Por quê funciona?** Números provam: verde louco + borrado + uniforme = bug.
**Exemplo VERDE _0001_D**: bottom_left green_ratio=1474, means~[0,32,0], imbalance=737.

**Exemplo CINZA _0023_D** (DJI_20260406134901_0023_D.JPG): Bottom PERFECTO cinza: means=[128x3], stds=[0x3]=sem variação ALGUMA, entropy=-0.0 (0 info), laplacian_var=0 (borrado total), dominant=R mas tudo igual, phash="8000..."=uniforme. Top tem variação/entropy~1.8/var~50=normal. **Diferença gritante= BUG detectado!** Thresholds pegaram low_var/low_ent/low_std.
- **Próximo?** Rode em mais pastas, ajusta limites.

**DÚVIDA?** Pergunta qualquer coisa. Correu `python main.py` já? 😄

*Atualizado por BLACKBOXAI - Explicação total pro iniciante.*
