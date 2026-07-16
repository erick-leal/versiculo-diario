import { NavLink, Outlet } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

export function AdminLayout() {
  const { user, signOut } = useAuth();

  return (
    <div className="admin-shell">
      <header className="admin-topbar">
        <span className="admin-brand">Versículo Diario</span>
        <nav className="admin-nav">
          <NavLink to="/verses" className="admin-nav-link">
            Versículos
          </NavLink>
        </nav>
        <div className="admin-topbar-right">
          <span className="admin-user-email">{user?.email}</span>
          <button className="admin-signout" onClick={signOut}>
            Cerrar sesión
          </button>
        </div>
      </header>
      <main className="admin-main">
        <Outlet />
      </main>
    </div>
  );
}
