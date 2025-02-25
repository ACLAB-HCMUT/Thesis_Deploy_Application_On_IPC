// import React, { createContext, useContext, useState } from "react"
// import { ChevronFirst, ChevronLast, MoreVertical } from 'lucide-react'
// // import Logo from '../../assets/image/logo.png'
// const Logo = require("../../assets/image/logo.png")

// const SidebarContext = createContext({ expanded: true })
// export default function Sidebar({children}) {
//     const [expanded, setExpanded] = useState(true)
//     return (
//         <aside className="h-screen">
//             <nav className="h-full inline-flex flex-col justify-between items-center bg-white border-r shadow-sm">
//                 <div className="p-4 pb-2 flex justify-between items-center">
//                     <img 
//                         src={Logo}
//                         className={`overflow-hidden transition-all size-11`} 
//                         alt="" 
//                     />
//                 </div>

//                 <SidebarContext.Provider value={{expanded}}>
//                     <ul className="px-3 flex flex-col justify-around">{children}</ul>
//                 </SidebarContext.Provider>

//                 <div className="border-t flex p-3">
//                     <img src="https://ui-avatars.com/api/?background=c7d2fe&color=3730a3&bold=true" className="w-10 h-10 rounded-md" alt="" />
//                 </div>
//             </nav>
//         </aside>
//     )
// }

// export function SidebarItem({icon, text, active, alert}) {
//     return (
//         <li className={`
//             relative flex items-center py-2 px-3 my-1
//             font-medium rounded-md cursor-pointer
//             transition-colors group
//             ${
//                 active
//                 ? "bg-gradient-to-tr from-indigo-200 to-indigo-100 text-indigo-800"
//                 : "hover:bg-indigo-50 text-gray-600"
//             }
//         `}>
//             {icon}
//             <span className={`overflow-hidden transition-all w-0`}>{text}</span>
//             {alert && <div className={`absolute right-2 w-2 h-2 rounded bg-indigo-400`}/>}

//             <div className={`
//                 absolute left-full rounded-md px-2 py-1 ml-6    
//                 bg-indigo-100 text-indigo-800 text-sm
//                 invisible opacity-20 -translate-x-3 transition-all
//                 group-hover:visible group-hover:opacity-100 group-hover:translate-x-0
//             `}>{text}</div>
//         </li>
//     )
// }
// src/components/Sidebar/index.tsx
import React, { createContext, useContext, useState } from "react"
import { useNavigate } from "react-router-dom"
const Logo = require("../../assets/image/logo.png")

const SidebarContext = createContext({ expanded: true })

export default function Sidebar({children}) {
    const [expanded, setExpanded] = useState(true)
    return (
        <aside className="h-screen">
            <nav className="h-full inline-flex flex-col justify-between items-center bg-white border-r shadow-sm">
                <div className="p-4 pb-2 flex justify-between items-center">
                    <img 
                        src={Logo}
                        className={`overflow-hidden transition-all size-11`} 
                        alt="" 
                    />
                </div>

                <SidebarContext.Provider value={{expanded}}>
                    <ul className="px-3 flex flex-col justify-around">{children}</ul>
                </SidebarContext.Provider>

                <div className="border-t flex p-3">
                    <img src="https://ui-avatars.com/api/?background=c7d2fe&color=3730a3&bold=true" className="w-10 h-10 rounded-md" alt="" />
                </div>
            </nav>
        </aside>
    )
}

export function SidebarItem({icon, text, active, alert, to}) {
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
            <span className={`overflow-hidden transition-all w-0`}>{text}</span>
            {alert && <div className={`absolute right-2 w-2 h-2 rounded bg-indigo-400`}/>}

            <div className={`
                absolute left-full rounded-md px-2 py-1 ml-6    
                bg-indigo-100 text-indigo-800 text-sm
                invisible opacity-20 -translate-x-3 transition-all
                group-hover:visible group-hover:opacity-100 group-hover:translate-x-0
            `}>{text}</div>
        </li>
    )
}