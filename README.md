# web-scraping-playwright
A Python web scraping project using Playwright to automatically collect posts from the Samsung Brasil X (Twitter) profile. The script extracts tweet text, publication date, likes, and repost counts, then organizes the data into a structured CSV file for analysis.

## Example Output
autor, descricao, data, curtidas, reposts
SamsungBrasil, #FeitoComGalaxy por @olhoquieto  — Calmaria.   #withGalaxy, 06/03/2026 23:08:47, 12, 1
SamsungBrasil, #FeitoComGalaxy por @olhoquieto  — Ângulo.   #withGalaxy, 06/03/2026 23:08:25, 14, 1
SamsungBrasil, #FeitoComGalaxy por  @jao .fritsch  — Liberdade.   #withGalaxy, 06/03/2026 23:07:55, 13, 0

# Technologies
- Python
- Playwright
- Pandas
- Asyncio

## Usage
Install dependencies:
```bash
pip install playwright pandas
playwright install
playwright install chromium
