import React from 'react';
import {
    Menu
} from 'lucide-react';

export default function Header({toggleSidebar}) {
    return (
        <nav className='fixed top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700'>
            <div className="px-3 py-3 lg:px-5 lg:pl-3">
                <div className="flex items-center justify-between">
                    <div className="flex items-center justify-start rtl:justify-end">
                        <button className='inline-flex items-center p-2 text-sm text-gray-500 rounded-lg lg:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200' onClick={toggleSidebar}>
                            <Menu className='text-2xl'/>
                        </button>
                        <a href="#" className="flex ms-2 md:me-24">
                            <img
                                src="https://img.logoipsum.com/243.svg"
                                className='h-8 me-3'
                                alt=""
                            />
                        </a>
                    </div>
                </div>
            </div>
        </nav>
    )
}