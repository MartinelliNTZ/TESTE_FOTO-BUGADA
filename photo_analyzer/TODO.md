def diagnostico(imagem_json):
    if not imagem_json["corrupted"]:
        return "OK", ""
    
    # Verifica se as regiões inferiores são cinzento puro (128,0)
    regioes = ["bottom_left", "bottom_right"]
    inferiores_cinzento = all(
        imagem_json[r]["means_R"] == 128 and
        imagem_json[r]["means_G"] == 128 and
        imagem_json[r]["means_B"] == 128 and
        imagem_json[r]["stds_R"] == 0
        for r in regioes
    )
    
    if inferiores_cinzento:
        # Verifica se as superiores também estão afetadas
        superiores_var = any(
            imagem_json[r]["mean_std"] > 1.0
            for r in ["top_left", "top_right"]
        )
        if superiores_var:
            detalhe = "Metade inferior em falta; parte superior com pouca informação"
        else:
            detalhe = "Metade inferior completamente em falta"
    else:
        # Outro tipo de corrupção (ex.: entropia muito baixa)
        if imagem_json["overall"]["entropy"] < 1.0:
            detalhe = "Imagem praticamente sem detalhe (possível corrupção geral)"
        else:
            detalhe = "Corrupção detectada (padrão não específico)"
    
    return "Corrompida", detalhe