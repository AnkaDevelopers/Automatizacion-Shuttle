def formatear_config(cfg_tuple):
    gps, glo, gal, bds = cfg_tuple
    def t(b): return "Use" if b else "Don't Use"
    return f"GPS={t(gps)}, GLO={t(glo)}, GAL={t(gal)}, BDS={t(bds)}"