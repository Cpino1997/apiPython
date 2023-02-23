import Head from 'next/head';
import {useState} from "react";
import {useRouter} from "next/router";

export default function Home() {
    const [usuario, setUsuario] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const router = useRouter();
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        const response = await fetch(process.env.API_ENDPOINT+'/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ usuario, password }),
        });

        if (response.ok) {
            const data = await response.json();
            const access_token = data.access_token;
            localStorage.setItem('access_token', access_token);
            setIsLoggedIn(true);
            await router.push('/dashboard');
        } else {
            const { mensaje } = await response.json();
            setError(mensaje);
        }
    };
  return (
    <>
      <Head >
        <title>Cliente</title>
        <meta name="description" content="Created by education only" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main>
          {isLoggedIn ? (
              <p>te encuentras logeado! ...</p>
          ) : (
         <div className="container mt-5">
             <div className="row justify-content-center">
                 <div className="col-md-6">
                     <div className="card">
                         <div className="card-header">
                             <h4 className="card-title">Inicio de sesión</h4>
                         </div>
                         <div className="card-body">
                             {error && (
                                 <div className="alert alert-danger" role="alert">
                                     {error}
                                 </div>
                             )}
                             <form onSubmit={handleSubmit}>
                                 <div className="form-group">
                                     <label htmlFor="usuario">Usuario</label>
                                     <input
                                         type="text"
                                         className="form-control"
                                         id="usuario"
                                         value={usuario}
                                         onChange={(event) => setUsuario(event.target.value)}
                                     />
                                 </div>
                                 <div className="form-group">
                                     <label htmlFor="password">Contraseña</label>
                                     <input
                                         type="password"
                                         className="form-control"
                                         id="password"
                                         value={password}
                                         onChange={(event) => setPassword(event.target.value)}
                                     />
                                 </div>
                                 <button type="submit" className="btn btn-primary">
                                     Iniciar sesión
                                 </button>
                             </form>
                         </div>
                     </div>
                 </div>
             </div>
         </div>
          )}
      </main>
    </>
  )
}