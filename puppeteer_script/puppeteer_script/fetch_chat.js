const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const url = process.argv[2] || 'https://grok.com/chat/233e673e-3426-45bd-86a2-32b43a0c2843';
  const outputFile = '/home/archangel/simple_bot_env/chat_history.txt';

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124');
  
  try {
    await page.goto(url, { waitUntil: 'networkidle2' });
    const content = await page.content();
    fs.writeFileSync(outputFile, content);
    console.log(`Opgeslagen in ${outputFile}: ${content.slice(0, 100)}...`);
  } catch (e) {
    console.error(`Fout bij scrapen: ${e}`);
  } finally {
    await browser.close();
  }
})();