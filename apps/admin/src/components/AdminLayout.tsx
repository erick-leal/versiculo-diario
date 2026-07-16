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
          <NavLink to="/reflections" className="admin-nav-link">
            Reflexiones
          </NavLink>
          <NavLink to="/schedule" className="admin-nav-link">
            Calendario
          </NavLink>
          <NavLink to="/media" className="admin-nav-link">
            Fondos
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
