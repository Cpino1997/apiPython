import { useEffect, useState } from "react";
import { useRouter } from "next/router";

export default function Perfil() {
    const [cuenta, setCuenta] = useState({});
    const [isError, setIsError] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [password, setPassword] = useState("");
    const [isUpdating, setIsUpdating] = useState(false);

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

    const handleChangePasswordClick = () => {
        setIsModalOpen(true);
    };

    const handleModalClose = () => {
        setIsModalOpen(false);
        setPassword("");
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSave = async () => {
        setIsUpdating(true);
        const access_token = localStorage.getItem("access_token");
        const headers = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${access_token}`,
        };
        const body = JSON.stringify({ ...cuenta, password });
        try {
            const response = await fetch(process.env.API_ENDPOINT + "/cuentas/update", {
                method: "PUT",
                headers,
                body,
            });
            if (!response.ok) {
                throw new Error("Error al actualizar cuenta");
            }
            const data = await response.json();
            setCuenta(data);
            setIsModalOpen(false);
        } catch (error) {
            setIsError(true);
        } finally {
            setIsUpdating(false);
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
        return <div>Error al cargar cuentas</div>;
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
            <button className={"btn btn-primary"} onClick={handleChangePasswordClick}>
                Cambiar Contraseña
            </button>
            {isModalOpen && (
                <div className={"modal"}>
                    <div className={"modal-content"}>
                        <div className={"modal-header"}>
                            <h4>Cambiar Contraseña</h4>
                            <button className={"btn-close"} onClick={handleModalClose} />
                        </div>
                        <div className={"modal-body"}>
                            <label>Nueva contraseña: </label>
                            <input type={"password"} value={password} onChange={handlePasswordChange} />
                        </div>
                        <div className={"modal-footer"}>
                            {!isUpdating ? (
                                <>
                                    <button className={"btn btn-secondary"} onClick={handleModalClose}>
                                        Cancelar
                                    </button>
                                    <button className={"btn btn-primary"} onClick={handleSave}>
                                        Guardar
                                    </button>
                                </>
                            ) : (
                                <button className={"btn btn-primary"} disabled>
                                    Actualizando...
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}