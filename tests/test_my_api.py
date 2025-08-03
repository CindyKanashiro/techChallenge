import requests
import json

BASE_URL = "http://localhost:8000/api/v1/books"

def test_endpoint(name, url, method="GET"):
    """Testa um endpoint e mostra o resultado"""
    print(f"\n🧪 Testando: {name}")
    print(f"📍 URL: {url}")
    print("-" * 50)
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, timeout=10)
        
        print(f"✅ Status: {response.status_code}")
        print(f"⏱️  Tempo: {response.elapsed.total_seconds():.2f}s")
        
        try:
            data = response.json()
            if isinstance(data, list):
                print(f"📊 Quantidade: {len(data)} items")
                if len(data) > 0:
                    print(f"📝 Primeiro item: {json.dumps(data[0], indent=2, ensure_ascii=False)[:200]}...")
            elif isinstance(data, dict):
                print(f"📝 Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
            else:
                print(f"📝 Resposta: {data}")
        except:
            print(f"📝 Resposta (texto): {response.text[:200]}...")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: API não está rodando! Execute: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERRO: {e}")

def main():
    print("🚀 TESTANDO ENDPOINTS DA API DE LIVROS")
    print("=" * 60)
    
    # Lista de testes baseados no seu banco de dados
    tests = [
        ("Todos os livros (limitado a 3)", f"{BASE_URL}/?limit=3"),
        ("Livro específico - A Light in the Attic", f"{BASE_URL}/1"),
        ("Livro específico - Tipping the Velvet", f"{BASE_URL}/2"),
        ("Todas as categorias", f"{BASE_URL}/categories/"),
        # ("Livros de Poetry", f"{BASE_URL}/?category=Poetry"),
        # ("Livros de Fiction", f"{BASE_URL}/?category=Fiction"),
        # ("Livros de History", f"{BASE_URL}/?category=History"),
        # ("Estatísticas", f"{BASE_URL}/stats/"),
        ("Buscar livro inexistente", f"{BASE_URL}/9999"),
    ]
    
    for name, url in tests:
        test_endpoint(name, url)
    
    print(f"\n{'=' * 60}")
    print("🎉 TESTES CONCLUÍDOS!")
    print("💡 Para mais detalhes, acesse: http://localhost:8000/docs")

if __name__ == "__main__":
    main()