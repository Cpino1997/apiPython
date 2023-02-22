import Link from 'next/link';
import { useRouter } from 'next/router';
import Head from "next/head";

const Navbar = () => {
    const router = useRouter();

    const handleLogout = async () => {
        try {
            const response = await fetch(process.env.API_ENDPOINT + "/auth/logout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            });
            if (response.ok) {
                localStorage.removeItem("access_token");
                await router.push("/");
            } else {
                const { mensaje } = await response.json();
                alert(mensaje);
            }
        } catch (error) {
            alert(error.message);
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
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark w-100">
            <div className="container">
                <Link href="/" className="navbar-brand">Cliente</Link>
                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse text-center" id="navbarNav">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <Link href="/dashboard"  className={`nav-link ${router.pathname === '/dashboard' && 'active'}`}>Inicio</Link>
                        </li>
                        <li className="nav-item">
                            <Link href="/cuentas" className={`nav-link ${router.pathname === '/cuentas' && 'active'}`}>Cuentas</Link>
                        </li>
                    </ul>
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <button className="btn btn-outline-light" onClick={handleLogout}>Salir</button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
        </>
    );
};

export default Navbar;
