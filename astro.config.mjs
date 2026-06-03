import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://ssoelpasotx.com',
  trailingSlash: 'always',
  build: { format: 'directory' },
  redirects: {
    '/social-security-office-el-paso': '/'
  }
});
