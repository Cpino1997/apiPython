import { useRouter } from 'next/router'
import { useState, useEffect } from 'react'
import Navbar from "@/pages/componentes/navbar";

export default function Cuenta() {
    const router = useRouter()
    const { id } = router.query
    const [cuenta, setCuenta] = useState(null)
    const [isLoading, setIsLoading] = useState(true)
    const [isError, setIsError] = useState(false)
    const [update, setUpdate] = useState(false)

    const handleUpdate = (e) => {
        e.preventDefault()
        setUpdate(true)
    }

    async function actualizarCuenta(cuentaActualizada, id) {
        
    }

    const handleSave = async () => {
        setUpdate(false)
        const cuentaActualizada = {
            usuario: document.getElementById("usuario").value,
            correo: document.getElementById("correo").value,
            roles: document.getElementById("roles").value
        }
        await actualizarCuenta(cuentaActualizada, id)
        getCuenta()
    }

    const getCuenta = async () => {
        try {
            const idNumerico = parseInt(id, 10);
            if (isNaN(idNumerico)) {
                await router.push('/cuentas');
                return;
            }
            const token = localStorage.getItem('access_token');
            const headers = {
                'Authorization': `Bearer ${token}`
            };
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
        return <div>Cargando...</div>
    }

    if (isError) {
        return <div>Error...</div>
    }

    return (
        <>
        <Navbar />
        <div className="d-flex justify-content-center align-items-center" style={{ height: "90vh" }}>
            <div className="card text-center" style={{ width: "25rem" }}>
                <div className="card-body">
                    <h5 className="card-title">Cuenta</h5>
                    <div className="form-group row g-3">
                        <div className="col-md-6">
                            <label htmlFor="usuario" className="form-label">Usuario</label>
                            {update ? (
                                <input type="text" className="form-control" id="usuario" defaultValue={cuenta.usuario} />
                            ) : (
                                <p>{cuenta.usuario}</p>
                            )}
                        </div>
                        <div className="col-md-6">
                            <label htmlFor="roles" className="form-label">Roles</label>
                            {update ? (
                                <input type="text" className="form-control" id="roles" defaultValue={cuenta.roles} />
                            ) : (
                                <p>{cuenta.roles}</p>
                            )}
                        </div>
                    </div>
                    <div className="form-group row g-3">
                        <div className="col-md-12">
                            <label htmlFor="correo" className="form-label">Correo</label>
                            {update ? (
                                <input type="email" className="form-control" id="correo" defaultValue={cuenta.correo} />
                            ) : (
                                <p>{cuenta.correo}</p>
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
                            <h1 className="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div className="modal-body">
                            ...
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" className="btn btn-primary">Save changes</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}
