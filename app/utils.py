import re
import json
import urllib.parse

def sanitize_chart_config(obj):
    """Remove funções JS proibidas para evitar erro no gráfico."""
    if isinstance(obj, dict):
        forbidden = ['formatter', 'callback', 'footer', 'afterBody']
        for key in forbidden:
            if key in obj: del obj[key]
        for key, value in list(obj.items()):
            sanitize_chart_config(value)
    elif isinstance(obj, list):
        for item in obj:
            sanitize_chart_config(item)

def process_response_text(raw_text):
    """Processa o Markdown e converte JSON de gráficos em Imagens."""
    # 1. Remove blocos SQL vazados
    text = re.sub(r'```sql.*?```', '', raw_text, flags=re.DOTALL)

    # 2. Converte JSON de Chart.js em Imagem (QuickChart)
    def json_to_chart(match):
        try:
            json_str = re.sub(r'//.*', '', match.group(1)).strip()
            json_str = re.sub(r'function\s*\(.*?\)\s*\{.*?\}', 'null', json_str, flags=re.DOTALL)
            js = json.loads(json_str)
            
            sanitize_chart_config(js)
            
            # Configuração padrão bonita
            if 'options' not in js: js['options'] = {}
            if 'plugins' not in js['options']: js['options']['plugins'] = {}
            js['options']['plugins']['datalabels'] = {
                'display': True, 'color': '#000', 'align': 'top', 'anchor': 'end', 
                'font': {'weight': 'bold'}
            }
            
            # URL Encode
            url = urllib.parse.quote(json.dumps(js, separators=(',', ':')))
            return f"\n![Gráfico Visual](https://quickchart.io/chart?c={url})\n"
        except Exception as e:
            return f""

    text = re.sub(r'```json(.*?)```', json_to_chart, text, flags=re.DOTALL)
    return text.replace("```", "").strip()