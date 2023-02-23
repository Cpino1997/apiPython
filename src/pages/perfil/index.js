import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";

export default function Perfil() {
    const [cuenta, setCuenta] = useState({});
    const [isError, setIsError] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    const router = useRouter();

    useEffect(() => {
        const access_token = localStorage.getItem("access_token");
        if (!access_token) {
            router.push("/");
        } else {
            const headers = {
                Authorization: `Bearer ${access_token}`,
            };
            fetchData(headers);
        }
    }, [router]);

    const fetchData = async (headers) => {
        try {
            const response = await fetch(process.env.API_ENDPOINT + "/cuentas/get", {
                headers,
            });
            if (!response.ok) {
                throw new Error("Error al cargar cuentas");
            }
            const data = await response.json();
            setCuenta(data);
        } catch (error) {
            setIsError(true);
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return (
            <div className={"container w-100"}>
                <p className={"text-center cargando"}>Cargando...</p>
            </div>
        );
    }

    if (isError) {
        return <div>Error al cargar el perfil</div>;
    }

    return (
        <div className={"container-fluid"}>
            <div className={"form-label"}>
                <label>Usuario : </label>
                <br/>
                <span>{cuenta.usuario}</span>
            </div>
            <div className={"form-label"}>
                <label>Correo electrónico: </label>
                <br />
                <span>{cuenta.correo}</span>
            </div>
            <Link
                className={"btn btn-primary"}
                href="/cuentas/[id]"
                as={`/cuentas/${cuenta.id}`}
            >
                Editar
            </Link>
        </div>
    );
}