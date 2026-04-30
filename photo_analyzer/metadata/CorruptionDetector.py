import json
import numpy as np
import imagehash
from metadata.ImageAnalyzer import ImageAnalyzer
from metadata.PhotoSector import PhotoSector
from pathlib import Path


class CorruptionDetector:
    def __init__(self, images_dir: str, bugged_patterns=None):
        self.dir = Path(images_dir)
        self.bugged_patterns = bugged_patterns or ['0001_D']
        self.analyzers = {}

    def load_images(self):
        jpgs = list(self.dir.rglob('*.JPG'))
        for jpg in jpgs:
            try:
                analyzer = ImageAnalyzer(str(jpg))
                self.analyzers[str(jpg)] = analyzer.get_full_metrics()
            except Exception as e:
                print(f"Error loading {jpg}: {e}")

    def is_corrupted(self, metrics: dict) -> bool:
        # Average bottom quadrants
        bl, br = metrics['bottom_left'], metrics['bottom_right']
        b_imbalance = (bl['channel_imbalance'] + br['channel_imbalance']) / 2
        b_var = (bl['laplacian_var'] + br['laplacian_var']) / 2
        b_ent = (bl['entropy'] + br['entropy']) / 2
        b_std_mean = (bl['mean_std'] + br['mean_std']) / 2
        
        # Average top quadrants
        tl, tr = metrics['top_left'], metrics['top_right']
        t_var = (tl['laplacian_var'] + tr['laplacian_var']) / 2
        
        # Thresholds
        imbalance_thresh = 4.0
        low_var_thresh = 50.0
        low_ent_thresh = 4.0
        low_std_thresh = 10.0
        quality_diff_thresh = 5.0
        
        # Check conditions
        imbalance_issue = b_imbalance > imbalance_thresh
        low_quality = b_var < low_var_thresh or b_ent < low_ent_thresh or b_std_mean < low_std_thresh
        quality_diff = t_var > b_var * quality_diff_thresh
        
        return imbalance_issue or low_quality or quality_diff

    def diagnostico(self, imagem_json):
        """
        Fornece diagnóstico detalhado sobre corrupção detectada.
        
        Returns: (status, detalhes, severidade, evidencias)
        """
        if not imagem_json.get("corrupted", False):
            return "OK", "", 0.0, []
        
        # Extrai métricas das regiões
        bl = imagem_json.get('bottom_left', {})
        br = imagem_json.get('bottom_right', {})
        tl = imagem_json.get('top_left', {})
        tr = imagem_json.get('top_right', {})
        
        # Verifica padrão: cinzento puro (128,128,128)
        means_bl = bl.get('means', (0, 0, 0))
        means_br = br.get('means', (0, 0, 0))
        
        # Converte para tupla se for lista
        if isinstance(means_bl, list):
            means_bl = tuple(means_bl)
        if isinstance(means_br, list):
            means_br = tuple(means_br)
        
        evidencias = []
        severidade = 0.0
        tipo_corrupacao = ""
        
        # 1. CINZENTO PURO (áreas inferiores (128,128,128) com stds=0)
        if (means_bl == (128.0, 128.0, 128.0) and means_br == (128.0, 128.0, 128.0) and
            bl.get('stds', (0, 0, 0))[0] < 1.0):
            
            superiores_var = (tl.get('mean_std', 0) > 1.0 or tr.get('mean_std', 0) > 1.0)
            
            if superiores_var:
                tipo_corrupacao = "Metade inferior em falta; parte superior com pouca informação"
                severidade = 0.85
                evidencias.append(f"Bottom cinzento puro: means=(128,128,128)")
            else:
                tipo_corrupacao = "Metade inferior completamente em falta"
                severidade = 0.95
                evidencias.append(f"Imagem praticamente vazia: fundo cinzento uniforme")
        
        # 2. VERDE EXTREMO (green_ratio muito alto)
        elif bl.get('green_ratio', 1) > 50 or br.get('green_ratio', 1) > 50:
            tipo_corrupacao = "Dominância de cor (verde) anormal"
            severidade = 0.75
            if bl.get('green_ratio', 1) > 50:
                evidencias.append(f"bottom_left: green_ratio={bl.get('green_ratio', 0):.1f}")
            if br.get('green_ratio', 1) > 50:
                evidencias.append(f"bottom_right: green_ratio={br.get('green_ratio', 0):.1f}")
        
        # 3. MUITO BORRADA (laplacian_var baixo)
        elif bl.get('laplacian_var', 100) < 50 or br.get('laplacian_var', 100) < 50:
            tipo_corrupacao = "Imagem excessivamente borrada ou uniforme"
            severidade = 0.65
            b_var = (bl.get('laplacian_var', 0) + br.get('laplacian_var', 0)) / 2
            t_var = (tl.get('laplacian_var', 0) + tr.get('laplacian_var', 0)) / 2
            evidencias.append(f"Nitidez crítica: bottom={b_var:.1f}, top={t_var:.1f}")
        
        # 4. ENTRADA MUITO BAIXA (entropy baixa)
        elif bl.get('entropy', 10) < 4.0 or br.get('entropy', 10) < 4.0:
            tipo_corrupacao = "Imagem com informação visual muito reduzida"
            severidade = 0.70
            b_ent = (bl.get('entropy', 0) + br.get('entropy', 0)) / 2
            evidencias.append(f"Entropia baixa: bottom={b_ent:.1f}")
        
        # 5. CORES SEM VARIAÇÃO (mean_std baixo)
        elif bl.get('mean_std', 100) < 10.0 or br.get('mean_std', 100) < 10.0:
            tipo_corrupacao = "Variação de cor praticamente nula"
            severidade = 0.60
            b_std = (bl.get('mean_std', 0) + br.get('mean_std', 0)) / 2
            evidencias.append(f"Mean std extremo: {b_std:.1f}")
        
        # Fallback
        else:
            tipo_corrupacao = "Corrupção detectada (padrão não específico)"
            severidade = 0.50
            if imagem_json.get('overall', {}).get('entropy', 0) < 1.0:
                evidencias.append("Entropia geral muito baixa")
        
        # Formata detalhes
        detalhes = tipo_corrupacao
        if evidencias:
            detalhes += " Evidências:  • " + "  • ".join(evidencias)
        
        return "Corrompida", detalhes, severidade, evidencias

    def detect(self):
        self.load_images()
        results = {}
        for path, metrics in self.analyzers.items():
            is_bug = self.is_corrupted(metrics)
            filename = Path(path).name
            
            # Adiciona flag de corrupção
            metrics['corrupted'] = is_bug
            
            # Gera diagnóstico detalhado
            status, detalhes, severidade, evidencias = self.diagnostico(metrics)
            metrics['diagnostico'] = {
                'status': status,
                'detalhes': detalhes,
                'severidade': severidade,
                'evidencias': evidencias
            }
            
            results[filename] = metrics
        return results

    def save_report(self, filename='detection_report.json'):
        results = self.detect()
        report_path = self.dir / filename
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str, ensure_ascii=False)
        print(f"Report saved: {report_path}")
        print(f"{'='*70}")
        print(f"{'RESUMO':<70}")
        print(f"{'='*70}")
        
        total = len(results)
        corrupted = sum(1 for d in results.values() if d.get('corrupted', False))
        
        print(f"Total de fotos: {total}")
        print(f"Corrompidas: {corrupted} ({corrupted/max(total,1)*100:.0f}%)")
        print(f"OK: {total - corrupted}")
        
        # Mostra fotos corrompidas
        if corrupted > 0:
            print(f"{'Fotos Corrompidas:':<70}")
            for fname, data in sorted(results.items()):
                if data.get('corrupted', False):
                    diag = data.get('diagnostico', {})
                    sev = diag.get('severidade', 0)
                    print(f"  ❌ {fname:<40} {sev*100:5.0f}%")
        
        print(f"{'='*70}")
        return results
