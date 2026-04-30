# Análise das Classes do Projeto Photo Analyzer

Este documento descreve todas as classes encontradas no projeto, incluindo sua localização, propósito principal e funcionalidades chave. Foram identificadas **5 classes** nos arquivos Python.

## Resumo Geral
| Arquivo              | Classe              | Tipo     | Propósito Principal |
|----------------------|---------------------|----------|---------------------|
| `hsv_util.py`       | `HSVUtil`          | Utility estática | Análise de regiões HSV (médias, desvios, dominância, entropia, nitidez) |
| `image_rgb_util.py` | `ImageRGBUtil`     | Utility estática | Análise completa RGB/HSV de imagem dividida em quadrantes |
| `image_analyzer.py` | `ImageAnalyzer`    | Wrapper  | Carrega imagem, EXIF e delega métricas para ImageRGBUtil |
| `corruption_detector.py` | `CorruptionDetector` | Principal | Detecta corrupção em fotos, gera relatório JSON com diagnósticos |
| `photo_sector.py`   | `PhotoSector`      | Modelo de dados | Armazena métricas de setor (quadrante), compatível com JSON |

## Detalhes por Classe

### 1. HSVUtil (`hsv_util.py`)
- **Tipo**: Classe com método estático único `analyze_hsv_region(region)`.
- **Função**: Converte região RGB para HSV e computa:
  - Médias e desvios padrão dos canais H, S, V.
  - Razões relativas entre canais, canal dominante e desbalanceamento.
  - Entropia no canal V, variância laplaciana (nitidez).
- **Uso**: Chamada internamente por ImageRGBUtil para análise HSV.

### 2. ImageRGBUtil (`image_rgb_util.py`)
- **Tipo**: Classe utilitária com métodos estáticos.
- **Métodos principais**:
  - `split_regions(image)`: Divide imagem em 4 quadrantes (TL, TR, BL, BR) + overall.
  - `analyze_color_region(region)`: Métricas RGB + HSV por região (médias/stds, ratios R/G/B, dominante, desbalanceamento, entropia, laplaciano, phash).
  - `get_full_metrics(...)`: Orquestra análise completa.
- **Saída**: Dict com métricas detalhadas por quadrante.
- **Dependências**: HSVUtil, imagehash, PIL.

### 3. ImageAnalyzer (`image_analyzer.py`)
- **Tipo**: Classe wrapper para análise de imagem individual.
- **Construtor**: Carrega imagem com OpenCV/PIL, extrai EXIF.
- **Método principal**: `get_full_metrics()` delega para `ImageRGBUtil.get_full_metrics()`.
- **Uso**: Consumida por CorruptionDetector.

### 4. CorruptionDetector (`corruption_detector.py`)
- **Tipo**: Classe principal de detecção.
- **Construtor**: Recebe diretório de imagens e padrões bugados opcionais.
- **Métodos**:
  - `load_images()`: Carrega todas *.JPG recursivamente, gera métricas.
  - `is_corrupted(metrics)`: Thresholds em quadrantes inferiores (desbalanceamento >4.0, baixa var/entropia/std).
  - `detect()`: Executa análise completa.
  - `save_report()`: Salva JSON + resumo console com diagnósticos (função auxiliar `diagnostico`).
- **Dependências**: ImageAnalyzer, PhotoSector.

### 5. PhotoSector (`photo_sector.py`)
- **Tipo**: Classe de modelo/dados para métricas de quadrante.
- **Construtor**: Parse de dict JSON (flattened ou raw), backward-compatible.
- **Atributos**: Médias/stds R/G/B, ratios, dominante, desbalanceamento, entropia, var para top_left (código parece incompleto/partial para um quadrante).
- **Método**: `to_json()` para serialização.
- **Uso**: Provavelmente para processar/validar dados de setores individuais do relatório JSON.

## Observações
- **Arquivos sem classes**: `main.py`, `generate_excel.py` (provavelmente scripts executáveis).
- **Fluxo típico**: CorruptionDetector → ImageAnalyzer → ImageRGBUtil (HSVUtil) → JSON report → PhotoSector para parsing.
- **Foco do projeto**: Detecção de corrupção em fotos (áreas cinzentas, borradas, baixa info visual).

Gerado automaticamente via análise de código (2023).

