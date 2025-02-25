import React, { createContext, useContext, useState } from "react"
import { Link } from "react-router-dom"
import { ChevronFirst, ChevronLast, MoreVertical } from 'lucide-react'
import Header from "../../components/common/Header.tsx";
const Logo = require("../../assets/image/logo.png")

const SidebarContext = createContext({ isExpanded: true })

import React, { createContext, useContext, useState } from "react"
import { useNavigate } from "react-router-dom"
const Logo = require("../../assets/image/logo.png")

export default function Sidebar({ children }) {
    const [isExpanded, setIsExpanded] = useState(false)
    const toggleSidebar = () => setIsExpanded((isExpanded) => !isExpanded)
    return (
        <div>
            <Header toggleSidebar={toggleSidebar}></Header>
            <aside className="h-screen">
                <nav className={`fixed top-0 left-0 z-40 pt-20 h-full flex flex-col bg-white border-r shadow-sm lg:translate-x-0 transition-transform ${isExpanded ? "translate-x-0" : "-translate-x-full"}`}>
                    {/* <div className="p-4 pb-2 flex justify-between items-center">
                        <img
                            src="https://img.logoipsum.com/243.svg"
                            className={`overflow-hidden transition-all ${
                            expanded ? "w-32" : "w-0"
                            }`}
                            alt=""
                        />
                        <button
                            onClick={() => setExpanded((curr) => !curr)}
                            className="p-1.5 rounded-lg bg-gray-50 hover:bg-gray-100"
                        >
                            {expanded ? <ChevronFirst /> : <ChevronLast />}
                        </button>
                    </div> */}

                    <SidebarContext.Provider value={{ isExpanded }}>
                    <ul className="flex-1 px-3">{children}</ul>
                    </SidebarContext.Provider>

                    <Link to="/profile">
                        <div className="border-t flex p-3">
                            <img
                                src="https://ui-avatars.com/api/?background=c7d2fe&color=3730a3&bold=true"
                                alt=""
                                className="w-10 h-10 rounded-md"
                            />
                            <div
                                className={`
                                flex justify-between items-center
                                overflow-hidden transition-all ${isExpanded ? "w-52 ml-3" : "w-0"}
                            `}
                            >
                                <div className="leading-4">
                                    <h4 className="font-semibold">John Doe</h4>
                                    <span className="text-xs text-gray-600">johndoe@gmail.com</span>
                                </div>
                                <MoreVertical size={20} />
                            </div>
                        </div>
                    </Link>
                </nav>
            </aside>
        </div>
        
    )
}


export function SidebarItem({ icon, text, active, alert, to}) {
    const { isExpanded } = useContext(SidebarContext)
    const navigate = useNavigate();
    const handleClick = () => {
        if (to) {
            navigate(to);
        }
    };

    return (
        <li 
            onClick={handleClick}
            className={`
                relative flex items-center py-2 px-3 my-1
                font-medium rounded-md cursor-pointer
                transition-colors group
                ${
                    active
                    ? "bg-gradient-to-tr from-indigo-200 to-indigo-100 text-indigo-800"
                    : "hover:bg-indigo-50 text-gray-600"
                }
            `}
        >

        {icon}
        <span
            className={`overflow-hidden transition-all ${
            isExpanded ? "w-52 ml-3" : "w-0"
            }`}
        >
            {text}
        </span>
        {alert && (
            <div
            className={`absolute right-2 w-2 h-2 rounded bg-indigo-400 ${
                isExpanded ? "" : "top-2"
            }`}
            />
        )}

        {!isExpanded && (
            <div
            className={`
            absolute left-full rounded-md px-2 py-1 ml-6
            bg-indigo-100 text-indigo-800 text-sm
            invisible opacity-20 -translate-x-3 transition-all
            group-hover:visible group-hover:opacity-100 group-hover:translate-x-0
        `}
            >
            {text}
            </div>
        )}
        </li>
    </Link>
    
    )
}