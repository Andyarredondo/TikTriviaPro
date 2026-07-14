import React from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import HostDashboard from "./pages/HostDashboard";
import ViewerOverlay from "./pages/overlay/ViewerOverlay";

export default function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Navigate to="/host" replace />} />
                <Route path="/host" element={<HostDashboard />} />
                <Route path="/overlay" element={<ViewerOverlay />} />
                <Route path="*" element={<Navigate to="/host" replace />} />
            </Routes>
        </BrowserRouter>
    );
}
