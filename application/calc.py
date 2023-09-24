from abc import abstractmethod

class Calc:
    """Classe responsavel pelos calculos matematicos"""
    def calcular(entry_text:str) -> float:
        """Realiza calculo com base no texto passado"""
        try:
            result = eval(entry_text)
            result = Calc._format_decimal(str(result))
            return result
        except Exception as err:
            print(err.args)
            return 0
        
    def _format_decimal(txt:str):
        if txt.find(".") > -1:
            split = txt.split(".")
            if split[1] == "0":
                txt = txt[:-2]
                return int(txt)
            return float(txt)
        return int(txt)
            