/** @type {import('next').NextConfig} */
const nextConfig = {
  // experimental: {
  //     serverActions: true,
  // },
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination: "http://0.0.0.0:8080/api/:path*",
        // NextJS's config customizes this to shill their serverless stuff and I don't care.
        //   destination:
        //     process.env.NODE_ENV === 'development'
        //       ? 'http://127.0.0.1:5328/api/:path*'
        //       : '/api/',
      },
    ];
  },
};

module.exports = nextConfig;
