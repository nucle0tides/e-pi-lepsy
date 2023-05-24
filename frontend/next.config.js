/** @type {import('next').NextConfig} */
const nextConfig = {}

module.exports = {
    async rewrites() {
        return [
            {
                source: "/:path*",
                destination: "http://0.0.0.0:8080/:path*"
            },
        ];
    },
};
