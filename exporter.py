import requests

def export_to_canva_autofill(metrics_data):
    """
    Интеграция с Canva Connect API (Autofill) для генерации презентации по шаблону.
    Документация: https://www.canva.dev/docs/connect/
    """
    canva_api_key = os.getenv("CANVA_API_KEY", "ваш_canva_api_token")
    template_id = os.getenv("CANVA_TEMPLATE_ID", "id_вашего_шаблона_в_canva")
    
    url = "https://api.canva.com/rest/v1/autofill" # Эндпоинт Canva Autofill API
    
    headers = {
        "Authorization": f"Bearer {canva_api_key}",
        "Content-Type": "application/json"
    }
    
    # Данные для заполнения полей шаблона Canva
    payload = {
        "brand_template_id": template_id,
        "data": {
            "total_revenue": {"type": "text", "text": metrics_data.get("sum_rev", "")},
            "max_deficit": {"type": "text", "text": metrics_data.get("max_deficit", "")},
            "net_profit": {"type": "text", "text": metrics_data.get("net_profit", "")},
            "roi_value": {"type": "text", "text": metrics_data.get("roi", "")}
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code in [200, 201, 202]:
            return response.json()
        else:
            print(f"Canva API Error [{response.status_code}]: {response.text}")
            return None
    except Exception as e:
        print(f"HTTP Request Exception (Canva): {e}")
        return None
