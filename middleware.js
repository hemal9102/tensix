// Vercel Routing Middleware: serve the Markdown twin of a page to agents that
// send "Accept: text/markdown". Browsers never send that, so they are untouched.
export const config = {
  matcher: ['/((?!api/|md/|assets/|\.well-known/).*)'],
};

export default async function middleware(request) {
  if (!(request.headers.get('accept') || '').includes('text/markdown')) return;
  const path = new URL(request.url).pathname.replace(/\/+$/, '') || '/';
  if (/\.[a-z0-9]+$/i.test(path)) return; // real files (robots.txt, script.js, ...)
  const mdPath = '/md/' + (path === '/' ? 'index' : path.slice(1)) + '.md';
  const res = await fetch(new URL(mdPath, request.url));
  if (res.status !== 200) return; // no Markdown twin: fall through to HTML
  return new Response(res.body, {
    headers: {
      'content-type': 'text/markdown; charset=utf-8',
      'vary': 'Accept',
      'x-markdown-source': mdPath,
    },
  });
}
