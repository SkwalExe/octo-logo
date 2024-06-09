import { defineConfig } from "vitepress";

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: "Octo-Logo",
    description:
        "A simple program that generates a logo for your open source project",
    srcDir: "src",
    themeConfig: {
        // https://vitepress.dev/reference/default-theme-config
        nav: [
            { text: "Home", link: "/" },
            { text: "Getting Started", link: "/getting-started" },
        ],
        search: {
            provider: "local",
        },
        editLink: {
            pattern: "https://github.com/skwalexe/octo-logo/edit/main/docs/src/:path",
        },
        sidebar: [
            {
                text: "Examples",
                items: [
                    { text: "Markdown Examples", link: "/markdown-examples" },
                    { text: "Runtime API Examples", link: "/api-examples" },
                ],
            },
        ],
        socialLinks: [
            { icon: "github", link: "https://github.com/SkwalExe/octo-logo" },
        ],
    },
});
