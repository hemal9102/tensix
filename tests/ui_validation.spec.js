const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test.describe('Principal UI/UX Validation', () => {
  
  test.beforeEach(async ({ page }) => {
    page.on('pageerror', exception => {
      console.error(`Uncaught exception: "${exception}"`);
    });
    page.on('console', msg => {
      if (msg.type() === 'error')
        console.error(`Console error: "${msg.text()}"`);
    });
    await page.goto('/');
  });

  test('should pass automated accessibility (WCAG) checks', async ({ page }) => {
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    // We expect 0 accessibility violations
    expect(accessibilityScanResults.violations, "WCAG Accessibility Violations found").toEqual([]);
  });

  test('should not have horizontal overflow (Responsiveness)', async ({ page }) => {
    const overflowX = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(overflowX, 'Page should not scroll horizontally. This indicates broken responsive design.').toBe(false);
  });

  test('should have a single H1 tag for SEO and screen readers', async ({ page }) => {
    const h1Count = await page.locator('h1').count();
    expect(h1Count, 'There should be exactly one H1 tag on the page to establish hierarchy.').toBe(1);
  });

  test('should have proper alt texts on all images', async ({ page }) => {
    const images = await page.locator('img');
    const count = await images.count();
    for (let i = 0; i < count; i++) {
      const alt = await images.nth(i).getAttribute('alt');
      expect(alt, `Image at index ${i} is missing an alt attribute.`).not.toBeNull();
    }
  });
});
