import React, {useState} from 'react';
import Sidebar, { SidebarItem } from "../../components/common/Sidebar.tsx";
import { House, TabletSmartphone, Bell, ShieldCheck, Settings, Pencil, Check} from "lucide-react";
import { Link } from "react-router-dom";

export default function Profile({ firstname, lastname, username, phone, gender, address }) {
    const [isEditing, setIsEditing] = useState(false);
    const [userData, setUserData] = useState({ firstname, lastname, username, phone, gender, address });

    const handleChange = (e) => {
        setUserData({ ...userData, [e.target.name]: e.target.value });
    };

    return (
        <main className="flex min-h-screen bg-gray-50">
            <Sidebar>
                <SidebarItem icon={<House size={20} />} text="Home" alert={false} active={undefined} to="home" />
                <SidebarItem icon={<TabletSmartphone size={20} />} text="Devices" alert={false} active={undefined} to="devices"/>
                <SidebarItem icon={<Bell size={20} />} text="Notification" alert={false} active={undefined} to="notification" />
                <SidebarItem icon={<Settings size={20} />} text="Settings" alert={false} active={undefined} to="settings" />
                <SidebarItem icon={<ShieldCheck size={20} />} text="Authenticate" alert={false} active={undefined} to="authenticate" />
            </Sidebar>
            <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
                {/* Avatar Section */}
            <div className="flex flex-row justify-between items-center">
                <div className="flex items-center space-x-4 p-4">
                    <img
                        src="https://ui-avatars.com/api/?background=c7d2fe&color=3730a3&bold=true"
                        alt="User Avatar"
                        className="w-16 h-16 rounded-full object-cover border-2 border-gray-300"
                    />
                    <div>
                        <h2 className="text-xl font-semibold text-gray-900">John Doe</h2>
                        <p className="text-gray-500">johndoe@gmail.com</p>
                    </div>
                </div>

                {/* Edit Button */}
                <button 
                onClick={() => setIsEditing(!isEditing)} 
                className="bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center hover:bg-blue-600"
                >
                    {isEditing ? <Check className="mr-2" /> : <Pencil className="mr-2" />} 
                    <div className='hidden sm:inline'>
                        {isEditing ? "Save" : "Edit"}
                    </div>
                
                </button>
            </div>

            {/* Form */}
            <div className="mt-4">
                <h3 className="text-xl font-medium mb-4">Profile</h3>
                <form className="bg-white p-6 rounded-lg shadow-md grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="mb-4">
                        <label className="block font-medium mb-2">First Name</label>
                        <input 
                            type="text" 
                            value={userData.firstname}
                            name="firstname"
                            onChange={handleChange}
                            readOnly={!isEditing} 
                            disabled={!isEditing} 
                            className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`} 
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block font-medium mb-2">Last Name</label>
                        <input 
                            type="text" 
                            value={userData.lastname} 
                            name="lastname"
                            readOnly={!isEditing}
                            disabled={!isEditing}
                            className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`} 
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block font-medium mb-2">Username</label>
                        <input 
                            type="text" 
                            value={userData.username} 
                            name="username"
                            readOnly={!isEditing} 
                            disabled={!isEditing} 
                            className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`} 
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block font-medium mb-2">Gender</label>
                        <input 
                            type="text" 
                            value={userData.gender}
                            name="gender" 
                            readOnly={!isEditing} 
                            disabled={!isEditing} 
                            className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`} 
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block font-medium mb-2">Phone Number</label>
                        <input 
                            type="text" 
                            value={userData.phone} 
                            name="phone"
                            readOnly={!isEditing} 
                            disabled={!isEditing} 
                            className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`} 
                        />
                    </div>
                    <div className="mb-4">
                        <label className="block font-medium mb-2">Address</label>
                        <input 
                            type="text" 
                            value={userData.address} 
                            name="address"
                            readOnly={!isEditing} 
                            disabled={!isEditing} 
                            className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`} 
                        />
                    </div>
                </form>
            </div>

            <div className="mt-4">
                <h3 className="text-lg font-medium text-gray-900">My email Address</h3>
                <div className="flex items-center space-x-4 p-4">
                    <span className="bg-blue-500 text-white w-8 h-8 flex items-center justify-center rounded-full text-sm">✉</span>
                    <div>
                        <h2 className="text-l font-semibold text-gray-900">johndoe@email.com</h2>
                        <p className="text-gray-500">1 month ago</p>
                    </div>
                </div>
            </div>
            </div>
        </main>   
    )
}