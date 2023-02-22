import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Navbar from "@/pages/componentes/navbar";
export default function Dashboard() {
    const router = useRouter();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const access_token = localStorage.getItem("access_token");
        if (!access_token) {
            router.push("/");
        } else {
            setIsLoading(false);
        }
    }, [router]);

    return (
        <>
            <Navbar></Navbar>
            <br/>
            {isLoading ? (
                <p>Cargando...</p>
            ) : (
                <div className={"container w-100"}>
                    <div className={"text-center"}>
                        <h1>¡Bienvenido al dashboard!</h1>
                        <p>Este es el contenido de la página de dashboard.</p>
                    </div>
                </div>
            )}
        </>
    );
}
