import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import Link from "next/link";
import Navbar from "@/pages/componentes/navbar";

export default function Cuentas() {
    const router = useRouter();
    const [cuentas, setCuentas] = useState([]);
    const [isError, setIsError] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

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
            const response = await fetch(process.env.API_ENDPOINT + '/cuentas', {
                headers,
            });
            if (!response.ok) {
                throw new Error("Error al cargar cuentas");
            }
            const data = await response.json();
            setCuentas(data);
        } catch (error) {
            setIsError(true);
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return <div>Cargando...</div>;
    }

    if (isError) {
        return <div>Error al cargar cuentas</div>;
    }

    return (
        <>
            <Navbar></Navbar>
            {isLoading ? (
                <p>Cargando...</p>
            ) : (
            <div className="container text-center mt-5 pt-2">
                <table className="table table-striped">
                    <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Correo</th>
                        <th>Roles</th>
                        <th>Acciones</th>
                    </tr>
                    </thead>
                    <tbody>
                    {Array.isArray(cuentas) &&
                        cuentas.map((cuenta) => (
                            <tr key={cuenta.id}>
                                <td>{cuenta.usuario}</td>
                                <td>{cuenta.correo}</td>
                                <td>{cuenta.roles}</td>
                                <td>
                                    <Link
                                        href="/cuentas/[id]"
                                        as={`/cuentas/${cuenta.id}`}
                                        className="btn btn-primary"
                                    >
                                        Editar
                                    </Link>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="d-flex justify-content-center">
                    <Link
                        href="/cuentas/nueva"
                        as={`/cuentas/nueva`}
                        type="button"
                        className="btn btn-primary"
                    >
                        Crear Cuenta
                    </Link>
                </div>
            </div>
            )}
        </>
    );
}
