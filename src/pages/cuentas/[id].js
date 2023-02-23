import {useRouter} from 'next/router'
import {useEffect, useState} from 'react'
import Navbar from "@/pages/componentes/navbar";
import Link from "next/link";


export default function Cuenta() {
    const router = useRouter()
    const { id } = router.query
    const [cuenta, setCuenta] = useState(null)
    const [isLoading, setIsLoading] = useState(true)
    const [isError, setIsError] = useState(false)
    const [update, setUpdate] = useState(false)
    const [usuario, setUsuario] = useState('');
    const [correo, setCorreo] = useState('');
    const [roles, setRoles] = useState('');
    const [password, setPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [isSuccess, setIsSuccess] = useState(false);

    function handleUpdate(e){
        e.preventDefault()
        setUpdate(true)
    }
    async function handleComprobar() {
        try {
            const idNumerico = parseInt(id, 10);
            const token = localStorage.getItem('access_token');
            const headers = {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            };
            const response = await fetch(process.env.API_ENDPOINT + `/auth/password/${idNumerico}`,{
                method: 'PUT',
                headers: headers,
                body: JSON.stringify({password:password, new_password:newPassword}),
            });
            console.log(response.mensaje)

        }catch (e) {
            setIsError(true)
            setIsLoading(false)
        }

    }


    async function actualizarCuenta(cuentaActualizada, id) {
        try {
            const idNumerico = parseInt(id, 10);
            const token = localStorage.getItem("access_token");
            const headers = {
                'Authorization': `Bearer ${token}`,
                "Content-Type": "application/json",
            };
            const res = await fetch(
                `${process.env.API_ENDPOINT}/cuentas/${idNumerico}`,
                {
                    method: "PUT",
                    headers: headers,
                    body: JSON.stringify(cuentaActualizada),
                }
            );
            const data = await res.json();
            setCuenta(data);
            setIsLoading(false);
            setIsSuccess(true);
            setTimeout(() => {
                setIsSuccess(false);
            }, 3000);
        } catch (e) {
            setIsError(true);
            setIsLoading(false);
        }
    }

    const handleSave = async () => {
        setUpdate(false);
        const cuentaActualizada = {
            usuario: usuario, correo: correo, roles: roles
        };
        await actualizarCuenta(cuentaActualizada, id);
        await getCuenta();
    };


    async function getCuenta() {
        try {
            const token = localStorage.getItem('access_token');
            const headers = {
                'Authorization': `Bearer ${token}`
            };
            const idNumerico = parseInt(id, 10);
            if (isNaN(idNumerico)) {
                await router.push('/cuentas');
                return;
            }
            const res = await fetch(process.env.API_ENDPOINT + `/cuentas/${idNumerico}`, {headers})
            const data = await res.json()
            setCuenta(data)
            setIsLoading(false)
        } catch (error) {
            setIsError(true)
            setIsLoading(false)
        }
    }

    useEffect(() => {
        getCuenta()
    }, [])

    if (isLoading) {
        return (
            <>
                <div className={"text-center m-5"}>
                    <div>Cargando...</div>
                </div>
            </>
        )
    }

    if (isError) {
        return (
            <>
                <Navbar></Navbar>
                <div className={"text-center m-5"}>
                    <p>Error al obtener la cuenta! ...</p>
                    <br />
                    <Link href={"/cuentas"} className={"btn btn-lg btn-outline-dark"} type={"button"}>Volver</Link>
                </div>
            </>
        )
    }
    return (
        <>
        <Navbar />
        <div className="d-flex justify-content-center align-items-center" style={{ height: "90vh" }}>
            <div className="card text-center" style={{ width: "25rem" }}>
                <div className="card-body">
                    <h5 className="card-title">Cuenta</h5>
                    <div className="form-group row g-3">
                        {isSuccess && (
                            <div className="col-md-12">
                                <div className="alert alert-success" role="alert">
                                    <div className={"text-center"}>La cuenta se actualizó con éxito.</div>
                                </div>
                            </div>
                        )}

                        <div className="col-md-6">
                            <label htmlFor="usuario" className="form-label">Usuario</label>
                            {update ? (
                                <input type="text" className="form-control" name={"usuario"} id="usuario" defaultValue={cuenta.usuario}
                                       onChange={(event) => setUsuario(event.target.value)}/>
                            ) : (
                                <p onChange={(event) => setUsuario(event.target.value)}>{cuenta.usuario}</p>
                            )}
                        </div>
                        <div className="col-md-6">
                            <label htmlFor="roles" className="form-label">Roles</label>
                            {update ? (
                                <input type="text" className="form-control" id="roles" defaultValue={cuenta.roles}
                                       onChange={(event) => setRoles(event.target.value)}/>
                            ) : (
                                <p onChange={(event) => setRoles(event.target.value)}>{cuenta.roles}</p>
                            )}
                        </div>
                    </div>
                    <div className="form-group row g-3">
                        <div className="col-md-12">
                            <label htmlFor="correo" className="form-label">Correo</label>
                            {update ? (
                                <input type="email" className="form-control" id="correo" defaultValue={cuenta.correo}
                                       onChange={(event) => setCorreo(event.target.value)}/>
                            ) : (
                                <p onChange={(event) => setCorreo(event.target.value)}>{cuenta.correo}</p>
                            )}
                        </div>
                    </div>
                    {update ? (
                        <div className="form-group row g-3">
                            <div className="col-12">
                                <button type="button" className="btn btn-primary" onClick={handleSave}>Guardar</button>
                            </div>
                        </div>
                    ) : (
                        <div className="form-group row g-3">
                            <div className="col-md-6">
                                <button className="btn btn-outline-primary " onClick={handleUpdate}>Actualizar</button>
                            </div>
                            <div className="col-md-6">
                                <button type="button" className="btn btn-outline-primary " data-bs-toggle="modal" data-bs-target="#exampleModal">Cambiar Contraseña</button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
            <div className="modal fade" id="exampleModal" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                <div className="modal-dialog modal-dialog-centered">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h1 className="modal-title fs-5" id="exampleModalLabel">Cambio de password</h1>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            <div className="form-group row g-3">
                                <div className="col-md-12">
                                    <label htmlFor="password" className="form-label">Contraseña</label>
                                    <input type="password"
                                           className="form-control"
                                           id="password"
                                           value={password}
                                           onChange={(event) => setPassword(event.target.value)} />
                                </div>
                                <div className="form-group row g-3">
                                    <div className="col-md-12">
                                        <label htmlFor="newPassword" className="form-label">Nueva Contraseña</label>
                                        <input type="password"
                                               className="form-control"
                                               id="newPassword"
                                               value={newPassword}
                                               onChange={(event) => setNewPassword(event.target.value)} />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" className="btn btn-primary" onClick={handleComprobar}>Cambiar Contraseña</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}
