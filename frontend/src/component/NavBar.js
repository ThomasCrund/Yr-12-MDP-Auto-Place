import React from 'react'

export default function NavBar(props) {
    const NavItemStyle = {
        height: "100%",
        color: "white",
        padding: (60 - 21.5) / 2,
        cursor: "pointer"

    }

    return (
        <div style={{
            width: "100%",
            display: "flex",
            height: "60px",
            background: "#2C2C2C",

        }}>
            <div style={NavItemStyle} onClick={() => props.tabClick(0)}><span>Material Importer</span></div>
            <div style={NavItemStyle} onClick={() => props.tabClick(1)} ><span>Placer</span></div>
        </div>
    )
}
