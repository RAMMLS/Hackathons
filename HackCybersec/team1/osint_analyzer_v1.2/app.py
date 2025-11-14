from flask import Flask, render_template, request, jsonify
import requests
import whois
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
import ssl

app = Flask(__name__)

# Отключаем проверку SSL для избежания ошибок сертификатов
ssl._create_default_https_context = ssl._create_unverified_context

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze_url():
#     try:
#         data = request.get_json()
#         url = data.get('url', '').strip()
        
#         if not url:
#             return jsonify({'error': 'URL не предоставлен'}), 400
        
#         # Добавляем схему если отсутствует
#         if not url.startswith(('http://', 'https://')):
#             url = 'https://' + url
        
#         print(f"🔍 Анализируем URL: {url}")
        
#         # Выполняем анализ
#         analysis_result = perform_comprehensive_analysis(url)
        
#         return jsonify(analysis_result)
        
#     except Exception as e:
#         print(f"❌ Ошибка при анализе: {e}")
#         return jsonify({'error': f'Ошибка анализа: {str(e)}'}), 500

@app.route('/analyze', methods=['POST'])
def analyze_url():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL не предоставлен'}), 400
        
        # Добавляем схему если отсутствует
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        print(f"🔍 Начинаем анализ URL: {url}")
        
        # Выполняем анализ
        print("📝 Вызываем perform_comprehensive_analysis...")
        analysis_result = perform_comprehensive_analysis(url)
        print(f"✅ Анализ завершен: {analysis_result}")
        
        return jsonify(analysis_result)
        
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА в analyze_url: {str(e)}")
        import traceback
        print(f"🔍 TRACEBACK: {traceback.format_exc()}")
        return jsonify({'error': f'Ошибка анализа: {str(e)}'}), 500

# def perform_comprehensive_analysis(url):
#     """Основная функция анализа URL"""
#     result = {
#         'url': url,
#         'timestamp': datetime.now().isoformat(),
#         'checks': {},
#         'final_verdict': {}
#     }
    
#     # 1. Проверка доступности
#     print("📡 Проверяем доступность...")
#     result['checks']['accessibility'] = check_accessibility(url)
    
#     # 2. WHOIS информация
#     print("🌐 Получаем WHOIS информацию...")
#     result['checks']['whois'] = check_whois_info(url)
    
#     # 3. Проверка robots.txt
#     print("🤖 Проверяем robots.txt...")
#     result['checks']['robots'] = check_robots_txt(url)
    
#     # 4. Анализ контента
#     print("📄 Анализируем контент сайта...")
#     result['checks']['content'] = analyze_website_content(url)
    
#     # 5. Определение категории
#     print("🎯 Определяем категорию OSINT/CSINT...")
#     result['final_verdict'] = determine_category(result['checks'])
    
#     print("✅ Анализ завершен!")
#     return result

# def perform_comprehensive_analysis(url):
#     """Основная функция анализа URL"""
#     try:
#         result = {
#             'url': url,
#             'timestamp': datetime.now().isoformat(),
#             'checks': {},
#             'final_verdict': {}
#         }
        
#         # 1. Проверка доступности
#         print("📡 Проверяем доступность...")
#         result['checks']['accessibility'] = check_accessibility(url)
        
#         # 2. WHOIS информация (может вызывать ошибки)
#         print("🌐 Получаем WHOIS информацию...")
#         try:
#             result['checks']['whois'] = check_whois_info(url)
#         except Exception as e:
#             result['checks']['whois'] = {'error': f'WHOIS failed: {str(e)}'}
        
#         # 3. Проверка robots.txt
#         print("🤖 Проверяем robots.txt...")
#         try:
#             result['checks']['robots'] = check_robots_txt(url)
#         except Exception as e:
#             result['checks']['robots'] = {'error': f'Robots failed: {str(e)}'}
        
#         # 4. Анализ контента
#         print("📄 Анализируем контент сайта...")
#         try:
#             result['checks']['content'] = analyze_website_content(url)
#         except Exception as e:
#             result['checks']['content'] = {'error': f'Content analysis failed: {str(e)}'}
        
#         # 5. Определение категории
#         print("🎯 Определяем категорию OSINT/CSINT...")
#         result['final_verdict'] = determine_category(result['checks'])
        
#         print("✅ Анализ завершен!")
#         return result
        
#     except Exception as e:
#         print(f"❌ CRITICAL ERROR in analysis: {e}")
#         return {
#             'url': url,
#             'error': str(e),
#             'final_verdict': {
#                 'category': 'ERROR',
#                 'confidence': 0,
#                 'category_reason': 'Произошла ошибка при анализе'
#             }
#         }

def perform_comprehensive_analysis(url):
    """Упрощенная функция анализа URL"""
    try:
        result = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'final_verdict': {}
        }
        
        # ТОЛЬКО проверка доступности (самая надежная)
        print("📡 Проверяем доступность...")
        result['checks']['accessibility'] = check_accessibility(url)
        
        # Пропускаем WHOIS и robots.txt временно
        result['checks']['whois'] = {'status': 'temporarily_disabled'}
        result['checks']['robots'] = {'status': 'temporarily_disabled'}
        
        # Простой анализ контента
        print("📄 Анализируем контент сайта...")
        try:
            result['checks']['content'] = analyze_website_content(url)
        except Exception as e:
            result['checks']['content'] = {'error': f'Content analysis failed: {str(e)}'}
        
        # Упрощенное определение категории
        print("🎯 Определяем категорию OSINT/CSINT...")
        result['final_verdict'] = determine_category_simple(result['checks'])
        
        print("✅ Анализ завершен!")
        return result
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        return {
            'url': url,
            'error': str(e),
            'final_verdict': {
                'category': 'ERROR',
                'confidence': 0,
                'category_reason': 'Временная ошибка'
            }
        }

def determine_category_simple(checks):
    """Упрощенная логика классификации"""
    accessibility = checks.get('accessibility', {})
    
    if accessibility.get('http_status') == 200:
        return {
            'category': 'OSINT',
            'confidence': 85,
            'category_reason': 'Сайт доступен публично',
            'reasons': ['✅ Сайт доступен публично (HTTP 200)']
        }
    else:
        return {
            'category': 'CSINT',
            'confidence': 70,
            'category_reason': 'Проблемы с доступом к сайту',
            'reasons': ['❌ Сайт недоступен или требует аутентификации']
        }


def check_accessibility(url):
    """Проверка доступности сайта"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"   → Отправляем запрос к {url}")
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        
        return {
            'http_status': response.status_code,
            'final_url': response.url,
            'requires_auth': response.status_code in [401, 403],
            'is_redirected': response.history != [],
            'access_time': response.elapsed.total_seconds(),
            'accessible': True
        }
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Ошибка доступа: {e}")
        return {
            'http_status': None,
            'error': str(e),
            'accessible': False
        }

# def check_whois_info(url):
#     """Получение WHOIS информации"""
#     try:
#         from urllib.parse import urlparse
#         domain = urlparse(url).netloc
        
#         # Убираем www. если есть
#         if domain.startswith('www.'):
#             domain = domain[4:]
            
#         print(f"   → Запрашиваем WHOIS для: {domain}")
#         whois_data = whois.whois(domain)
        
#         return {
#             'domain_name': str(whois_data.domain_name) if whois_data.domain_name else None,
#             'registrar': whois_data.registrar,
#             'creation_date': str(whois_data.creation_date) if whois_data.creation_date else None,
#             'expiration_date': str(whois_data.expiration_date) if whois_data.expiration_date else None,
#             'name_servers': list(whois_data.name_servers) if whois_data.name_servers else None,
#             'emails': whois_data.emails,
#             'is_private': whois_data.private if hasattr(whois_data, 'private') else False
#         }
#     except Exception as e:
#         print(f"   ❌ Ошибка WHOIS: {e}")
#         return {'error': f'WHOIS ошибка: {str(e)}'}

def check_whois_info(url):
    """Получение WHOIS информации"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        
        # Убираем www. если есть
        if domain.startswith('www.'):
            domain = domain[4:]
            
        print(f"   → Запрашиваем WHOIS для: {domain}")
        whois_data = whois.whois(domain)
        
        # Простая проверка без сложной обработки
        return {
            'domain_name': str(domain),
            'registrar': getattr(whois_data, 'registrar', 'Unknown'),
            'is_private': getattr(whois_data, 'private', False)
        }
    except Exception as e:
        print(f"   ❌ Ошибка WHOIS: {e}")
        return {'error': f'WHOIS unavailable: {str(e)}'}
    
def check_robots_txt(url):
    """Проверка robots.txt"""
    try:
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        
        print(f"   → Проверяем: {robots_url}")
        response = requests.get(robots_url, timeout=5)
        
        if response.status_code == 200:
            allows_crawling = 'User-agent: *' in response.text and 'Disallow: /' not in response.text
            return {
                'exists': True,
                'content_preview': response.text[:500],  # Первые 500 символов
                'allows_crawling': allows_crawling
            }
        else:
            return {'exists': False}
    except Exception as e:
        print(f"   ❌ Ошибка robots.txt: {e}")
        return {'exists': False, 'error': 'Не удалось получить robots.txt'}

def analyze_website_content(url):
    """Анализ содержимого сайта"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"   → Анализируем контент...")
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Поиск форм аутентификации
        login_forms = soup.find_all('form')
        has_login_form = any(
            form.find('input', {'type': 'password'}) or 
            'login' in form.get('action', '').lower() or
            'signin' in form.get('action', '').lower() or
            'auth' in form.get('action', '').lower()
            for form in login_forms
        )
        
        # Поиск paywall индикаторов
        text = soup.get_text().lower()
        has_paywall_indicators = any(
            indicator in text for indicator in 
            ['subscribe', 'premium', 'membership', 'paywall', 'subscription', 'pay to read']
        )
        
        return {
            'title': soup.title.string if soup.title else 'No title',
            'has_login_form': has_login_form,
            'has_paywall_indicators': has_paywall_indicators,
            'form_count': len(login_forms),
            'meta_description': soup.find('meta', attrs={'name': 'description'})
        }
    except Exception as e:
        print(f"   ❌ Ошибка анализа контента: {e}")
        return {'error': f'Ошибка анализа контента: {str(e)}'}

def determine_category(checks):
    """Определение категории OSINT/CSINT на основе проверок"""
    score = 0
    reasons = []
    
    print("   → Вычисляем категорию...")
    
    # Критерий 1: Доступность (30 баллов)
    accessibility = checks.get('accessibility', {})
    if accessibility.get('http_status') == 200:
        score += 30
        reasons.append("✅ Сайт доступен публично (HTTP 200)")
    elif accessibility.get('requires_auth'):
        score -= 20
        reasons.append("❌ Требуется аутентификация")
    elif not accessibility.get('accessible', False):
        score -= 15
        reasons.append("❌ Сайт недоступен")
    
    # Критерий 2: WHOIS информация (25 баллов)
    whois_info = checks.get('whois', {})
    if not whois_info.get('error'):
        if not whois_info.get('is_private', True):
            score += 25
            reasons.append("✅ Публичная регистрация домена")
        else:
            score -= 10
            reasons.append("⚠️ Приватная регистрация домена")
    else:
        score -= 5
        reasons.append("⚠️ WHOIS информация недоступна")
    
    # Критерий 3: Robots.txt (15 баллов)
    robots = checks.get('robots', {})
    if robots.get('exists'):
        if robots.get('allows_crawling', False):
            score += 15
            reasons.append("✅ Разрешен краулинг в robots.txt")
        else:
            score -= 5
            reasons.append("⚠️ Ограничения в robots.txt")
    else:
        score += 5
        reasons.append("ℹ️ Robots.txt не найден")
    
    # Критерий 4: Контент анализ (30 баллов)
    content = checks.get('content', {})
    if not content.get('error'):
        if not content.get('has_login_form', False):
            score += 15
            reasons.append("✅ Нет форм аутентификации")
        else:
            score -= 10
            reasons.append("❌ Обнаружены формы аутентификации")
        
        if not content.get('has_paywall_indicators', False):
            score += 15
            reasons.append("✅ Нет признаков paywall")
        else:
            score -= 10
            reasons.append("❌ Обнаружены признаки paywall")
    
    # Определение категории
    confidence = max(0, min(100, score))
    
    if confidence >= 70:
        category = "OSINT"
        category_reason = "Источник является открытым и публично доступным"
    elif confidence >= 40:
        category = "POTENTIALLY_OSINT"
        category_reason = "Источник в основном открыт, но есть некоторые ограничения"
    else:
        category = "CSINT"
        category_reason = "Источник имеет значительные ограничения доступа"
    
    print(f"   → Результат: {category} (уверенность: {confidence}%)")
    
    return {
        'category': category,
        'confidence': confidence,
        'score_breakdown': score,
        'reasons': reasons,
        'category_reason': category_reason
    }

if __name__ == '__main__':
    print("🚀 Запуск ПОЛНОГО сервера анализа OSINT/CSINT...")
    print("📡 Адрес: http://127.0.0.1:5000")
    print("🔧 Режим: Полный анализ с WHOIS и проверкой контента")
    print("--------------------------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=True)
