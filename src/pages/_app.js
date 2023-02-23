import { useEffect } from "react";
import { useRouter } from "next/router";
import 'bootstrap/dist/css/bootstrap.min.css';
import '/src/styles/estilos.css';

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    const VerificaToken = async () => {
      const access_token = localStorage.getItem("access_token");
      if (access_token) {
        const response = await fetch(process.env.API_ENDPOINT + "/auth/verify", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${access_token}`,
          },
        });
        if (!response.ok) {
          const { mensaje } = await response.json();
          if (mensaje === 'Token has expired') {
            try {
              const response2 = await fetch(process.env.API_ENDPOINT + "/auth/refresh", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                  "Authorization": `Bearer ${access_token}`,
                },
              });
              if (response2.ok) {
                const data = await response2.json();
                const new_access_token = data.access_token;
                localStorage.setItem("access_token", new_access_token);
                return true;
              } else {
                localStorage.removeItem("access_token");
                await router.push("/");
                return false;
              }
            } catch (error) {
              localStorage.removeItem("access_token");
              await router.push("/");
              return false;
            }
          } else {
            alert(mensaje);
            localStorage.removeItem("access_token");
            await router.push("/");
            return false;
          }
        }
      } else {
        await router.push("/");
        return false;
      }
    };

    VerificaToken().then(r => console.log(r));
    const interval = setInterval(VerificaToken, 300000); // check every minute
    return () => clearInterval(interval);
  }, [router]);

  useEffect(() => {
    require("bootstrap/dist/js/bootstrap.bundle.min.js");
  }, []);

  return <Component {...pageProps} />;
}

export default MyApp;
