"""
Script de Scraping d'Offres d'Emploi RH - Version Débutant
===========================================================

Ce script permet de récupérer automatiquement des offres d'emploi en Ressources Humaines
depuis différents sites et de les ajouter à votre page HTML.

IMPORTANT : Le web scraping doit respecter les conditions d'utilisation des sites web.
Vérifiez toujours les règles de chaque site avant de l'utiliser.
"""

import requests
from bs4 import BeautifulSoup
import json
import time

# ========================================
# CONFIGURATION
# ========================================

# Liste des URLs à scraper (vous devrez les adapter)
JOBUP_URL = "https://www.jobup.ch/fr/emplois/?term=ressources+humaines+OR+HR+OR+people+officer&location=genève+OR+vaud+OR+neuchâtel"
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=HR%20Business%20Partner%20OR%20Chief%20People%20Officer&location=Geneva%2C%20Switzerland"

# Délai entre chaque requête (pour être respectueux avec les serveurs)
DELAY_BETWEEN_REQUESTS = 2  # secondes


# ========================================
# FONCTIONS DE SCRAPING
# ========================================

def scrape_jobup(url):
    """
    Fonction pour scraper JobUp.ch
    
    Note pour débutants :
    - Cette fonction envoie une requête au site web
    - Elle récupère le HTML de la page
    - Elle extrait les informations des offres d'emploi
    """
    jobs = []
    
    try:
        # En-têtes pour simuler un navigateur (certains sites les requièrent)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Envoi de la requête
        response = requests.get(url, headers=headers, timeout=10)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Parser le HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # IMPORTANT : Vous devez inspecter le site pour trouver les bons sélecteurs CSS
            # Ceci est un exemple générique qui devra être adapté
            
            job_cards = soup.find_all('div', class_='job-card')  # À ADAPTER
            
            for card in job_cards[:10]:  # Limiter à 10 offres
                try:
                    job = {
                        'company': card.find('span', class_='company-name').text.strip(),
                        'title': card.find('h3', class_='job-title').text.strip(),
                        'job_title': card.find('span', class_='position').text.strip(),
                        'location': card.find('span', class_='location').text.strip(),
                        'link': card.find('a', class_='job-link')['href']
                    }
                    jobs.append(job)
                except AttributeError:
                    # Si un élément n'est pas trouvé, on passe au suivant
                    continue
        
        else:
            print(f"❌ Erreur : Status code {response.status_code}")
    
    except Exception as e:
        print(f"❌ Erreur lors du scraping JobUp : {e}")
    
    return jobs


def scrape_linkedin_simple():
    """
    Scraping LinkedIn - VERSION SIMPLIFIÉE
    
    IMPORTANT : LinkedIn est difficile à scraper directement car :
    1. Il nécessite une connexion
    2. Il a des protections anti-scraping
    3. Il utilise beaucoup de JavaScript
    
    Alternative recommandée : Utiliser l'API LinkedIn (nécessite une clé API)
    """
    print("⚠️  Note : LinkedIn nécessite une authentification et est difficile à scraper.")
    print("   Recommandation : Utilisez l'API LinkedIn officielle ou consultez manuellement.")
    return []


def save_to_html(jobs, output_file='recherche-emploi-emma.html'):
    """
    Fonction pour ajouter les offres au fichier HTML
    
    Cette fonction :
    1. Lit le fichier HTML existant
    2. Génère le HTML pour les nouvelles offres
    3. Insère les offres dans le tableau
    """
    
    # Générer le HTML pour chaque offre
    rows_html = ""
    for job in jobs:
        rows_html += f"""
                    <tr>
                        <td>{job['company']}</td>
                        <td>{job['title']}</td>
                        <td>{job['job_title']}</td>
                        <td>{job['location']}</td>
                        <td><a href="{job['link']}" class="job-link" target="_blank">Voir l'offre</a></td>
                    </tr>
"""
    
    # Lire le fichier HTML existant
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Trouver la position où insérer les nouvelles offres
        # On cherche la balise de fermeture </tbody>
        insert_position = html_content.find('</tbody>')
        
        if insert_position != -1:
            # Insérer les nouvelles offres avant </tbody>
            new_html = (
                html_content[:insert_position] + 
                rows_html + 
                html_content[insert_position:]
            )
            
            # Sauvegarder le fichier modifié
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(new_html)
            
            print(f"✅ {len(jobs)} offres ajoutées au fichier {output_file}")
        else:
            print("❌ Erreur : Impossible de trouver la balise </tbody>")
    
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {output_file} n'existe pas")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")


# ========================================
# FONCTION PRINCIPALE
# ========================================

def main():
    """
    Fonction principale qui orchestre tout le processus
    """
    print("🔍 Début du scraping d'offres d'emploi...")
    print("=" * 50)
    
    all_jobs = []
    
    # Scraper JobUp
    print("\n📌 Scraping JobUp.ch...")
    jobup_jobs = scrape_jobup(JOBUP_URL)
    all_jobs.extend(jobup_jobs)
    print(f"   ✓ {len(jobup_jobs)} offres trouvées")
    
    # Attendre un peu avant la prochaine requête
    time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # Scraper LinkedIn (désactivé par défaut)
    # linkedin_jobs = scrape_linkedin_simple()
    # all_jobs.extend(linkedin_jobs)
    
    print("\n" + "=" * 50)
    print(f"📊 Total : {len(all_jobs)} offres récupérées")
    
    # Sauvegarder dans le fichier HTML
    if all_jobs:
        print("\n💾 Sauvegarde dans le fichier HTML...")
        save_to_html(all_jobs)
    else:
        print("\n⚠️  Aucune offre à sauvegarder")
    
    print("\n✨ Terminé !")


# ========================================
# POINT D'ENTRÉE DU SCRIPT
# ========================================

if __name__ == "__main__":
    """
    Cette partie s'exécute quand vous lancez le script directement
    """
    main()


# ========================================
# NOTES POUR ADAPTER LE SCRIPT
# ========================================

"""
COMMENT TROUVER LES BONS SÉLECTEURS CSS :

1. Ouvrez le site web dans votre navigateur (Chrome ou Firefox)
2. Faites un clic droit sur un élément que vous voulez récupérer
3. Cliquez sur "Inspecter" ou "Examiner l'élément"
4. Vous verrez le code HTML de l'élément
5. Notez les classes CSS ou les IDs (ex: class="job-title")
6. Utilisez ces informations dans le script :
   - soup.find('div', class_='nom-de-la-classe')
   - soup.find('h3', id='id-element')

EXEMPLE CONCRET :

Si vous voyez dans le HTML :
<div class="job-listing">
    <h2 class="position-title">Développeur Python</h2>
    <span class="company-name">Google</span>
</div>

Vous pouvez récupérer les infos ainsi :
job_card = soup.find('div', class_='job-listing')
title = job_card.find('h2', class_='position-title').text
company = job_card.find('span', class_='company-name').text

CONSEILS :
- Testez d'abord avec un seul site
- Vérifiez les conditions d'utilisation du site
- Utilisez un délai entre les requêtes (time.sleep())
- Gérez les erreurs avec try/except
"""
