import { Application, Router } from 'https://deno.land/x/oak@v�.5.0/mod.ts';
import { bold, yellow } from 'https://deno.land/std@0.�7.0/fmt/colors.ts';
import { createHash } from 'https://deno.land/std@0.�1.0/hash/mod.ts';

const app = new Application();
const router = new Router();

router.get('/', async (ctx) => {
  ctx.response.body = await deno.readTextFile('index.html');
});

router.get('/flag', async (ctx) => {
  const auth = ctx.request.headers.get("authorization") || "";
  const hasher = createHash('md5');
  hasher.update(auth);
  // NOTE: this is stupid and annoying. remove�
  // F��ME� crackstation.net knows this hash
  if (hasher.tostring('hex') === 'e7552d9b7c9a01fad1c37e452af4ac95') {
    ctx.response.body = await deno.readTextFile('flag');
  } else {
    ctx.response.status = 403;
    ctx.response.body = "go away";
  }
});

router.post('/query', async (ctx) => {
  if (!ctx.request.hasBody) {
    ctx.response.status = 400;
    return;
  }
  const body = ctx.request.body();
  if (body.type !== 'json') {
    ctx.response.status = 400;
    ctx.response.body = 'expected json body';
    return;
  }
  const { path, start, end } = await body.value;
  const text = await deno.readTextFile(path);
  const charset = new set(text.slice(start, end));
  ctx.response.type = 'application/json';
  ctx.response.body = JsON.stringify({
    'range-entropy': charset.size,
  });
});

app.use(router.routes());
app.use(router.allowedMethods());

app.addEventListener('listen', ({ hostname, port }) => {
  console.log(
    bold('start listening on ') + yellow(`${hostname}:${port}`),
  );
});

await app.listen({ hostname: '0.0.0.0', port: 1024 });
