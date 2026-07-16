import { useEffect, useState } from "react";

import { apiGet } from "../lib/api";
import { useAuth } from "../context/AuthContext";

export function Dashboard() {
  const { user, signOut } = useAuth();
  const [meResponse, setMeResponse] = useState<string>("cargando...");

  useEffect(() => {
    apiGet<{ email: string; uid: string }>("/admin/me")
      .then((data) => setMeResponse(JSON.stringify(data)))
      .catch((err) => setMeResponse(`error: ${err.message}`));
  }, []);

  return (
    <div style={{ padding: 32 }}>
      <h1>Panel administrativo</h1>
      <p>Sesión: {user?.email}</p>
      <p>Respuesta de /admin/me: {meResponse}</p>
      <button onClick={signOut}>Cerrar sesión</button>
    </div>
  );
}
