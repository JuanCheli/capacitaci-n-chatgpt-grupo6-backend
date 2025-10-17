"""
Script de prueba para verificar que la API está funcionando correctamente.
Ejecutar después de iniciar el servidor con: python -m uvicorn api.main:app --reload
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*80 + "\n")

def test_endpoint(name: str, method: str, endpoint: str, data: Dict[str, Any] = None):
    """Función helper para probar endpoints"""
    print(f"🧪 Probando: {name}")
    print(f"   {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            print(f"   Datos: {json.dumps(data, ensure_ascii=False)}")
            response = requests.post(
                f"{BASE_URL}{endpoint}",
                json=data,
                headers={"Content-Type": "application/json"}
            )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Respuesta exitosa:")
            print(f"   {json.dumps(result, indent=2, ensure_ascii=False)[:500]}...")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ❌ Error: No se pudo conectar al servidor")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   python -m uvicorn api.main:app --reload")
        return False
    except Exception as e:
        print(f"   ❌ Error inesperado: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de la API del Simulador ChatGPT")
    print_separator()
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Endpoint raíz
    if test_endpoint("Endpoint raíz", "GET", "/"):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 2: Health check
    if test_endpoint("Health check", "GET", "/health"):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 3: Chat simulado - Prompt básico
    if test_endpoint(
        "Chat simulado - Prompt básico",
        "POST",
        "/simulador/chat",
        {"prompt": "¿Qué es la inteligencia artificial?"}
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 4: Chat simulado - Prompt vacío (debe fallar)
    print("🧪 Probando: Chat con prompt vacío (debe dar error)")
    if test_endpoint(
        "Chat con prompt vacío",
        "POST",
        "/simulador/chat",
        {"prompt": ""}
    ):
        tests_failed += 1
        print("   ⚠️  Esperábamos un error, pero tuvo éxito")
    else:
        tests_passed += 1
        print("   ✅ Error manejado correctamente")
    print_separator()
    
    # Test 5: RAG - Consulta sobre ChatGPT
    if test_endpoint(
        "RAG - ¿Qué es ChatGPT?",
        "POST",
        "/simulador/rag",
        {"question": "qué es chatgpt"}
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 6: RAG - Consulta sobre prompts
    if test_endpoint(
        "RAG - Consejos de prompting",
        "POST",
        "/simulador/rag",
        {"question": "cómo hacer buenos prompts"}
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 7: RAG - Consulta sobre seguridad
    if test_endpoint(
        "RAG - Seguridad con IA",
        "POST",
        "/simulador/rag",
        {"question": "seguridad privacidad"}
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 8: RAG - Consulta sin resultados
    if test_endpoint(
        "RAG - Consulta sin resultados",
        "POST",
        "/simulador/rag",
        {"question": "xyzabc123"}
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Test 9: RAG - Curso para adultos mayores
    if test_endpoint(
        "RAG - Información del curso",
        "POST",
        "/simulador/rag",
        {"question": "adultos mayores curso beneficios"}
    ):
        tests_passed += 1
    else:
        tests_failed += 1
    print_separator()
    
    # Resumen
    total_tests = tests_passed + tests_failed
    print("📊 RESUMEN DE PRUEBAS")
    print(f"   Total: {total_tests}")
    print(f"   ✅ Exitosas: {tests_passed}")
    print(f"   ❌ Fallidas: {tests_failed}")
    print(f"   Porcentaje de éxito: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_failed == 0:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
    else:
        print(f"\n⚠️  {tests_failed} prueba(s) fallaron. Revisa los errores arriba.")
    
    print_separator()

if __name__ == "__main__":
    main()
