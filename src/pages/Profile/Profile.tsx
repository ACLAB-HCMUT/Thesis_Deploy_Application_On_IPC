import React, { useState, useEffect } from "react";
import { House, TabletSmartphone, Bell, ShieldCheck, Settings, Pencil, Check, Phone } from "lucide-react";
import axios from "axios";
import { useLocation } from "react-router-dom";
// Hàm tạo chữ cái viết tắt
const getInitials = (firstName, lastName) => {
    const firstInitial = firstName?.charAt(0)?.toUpperCase() || '';
    const lastInitial = lastName?.charAt(0)?.toUpperCase() || '';
    return `${firstInitial}${lastInitial}`;
};

export default function Profile() {
    const [isEditing, setIsEditing] = useState(false);
    const [userData, setUserData] = useState({
        firstName: "",
        lastName: "",
        username: "",
        email: "",
        phone: "",
        address: "",
    });
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const location = useLocation(); // Lấy thông tin URL hiện tại
    // Thêm state để kiểm tra avatar (nếu bạn có logic kiểm tra avatar)
    const [hasAvatar, setHasAvatar] = useState(true); // Giả sử mặc định có avatar
    const userInitials = getInitials(userData.firstName, userData.lastName);
    useEffect(() => {
        const fetchUserData = async () => {
            setIsLoading(true);
            try {
                // const response = await axios.get("http://localhost:8001/api/auth/user-data", {
                    // const response = await axios.get("https://do-an-da-nganh.onrender.com/api/users/info", {
                    // headers: {
                    //     Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    // },
                    const response = await axios.get("https://do-an-da-nganh.onrender.com/api/users/info", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                        email: location.state?.email || '',
                    },
                });
                // if (response.data.success) {
                if (response.data) {
                    setUserData(response.data.data);
                    setHasAvatar(!!response.data.data.avatar || 
                        (response.data.firstName && response.data.lastName));
                } else {
                    setMessage("Không thể tải thông tin người dùng.");
                }
            } catch (error) {
                console.error("Lỗi khi lấy thông tin user:", error);
                setMessage(error.response?.data?.message || "Đã xảy ra lỗi khi tải thông tin.");
            } finally {
                setIsLoading(false);
            }
        };
        fetchUserData();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        if (name !== "email" && name !== "phone") {
            setUserData((prev) => ({ ...prev, [name]: value }));
        }
    };

    const handleSave = async () => {
        setIsLoading(true);
        try {
           
            //  const response = await axios.put("http://localhost:8001/api/auth/updateProfile", {
                const response = await axios.put("https://do-an-da-nganh.onrender.com/api/users/updateInfo", {    
                firstName: userData.firstName,
                lastName: userData.lastName,
                username: userData.username,
                address: userData.address,
                email: userData.email,
                phone: userData.phone
                }, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                },
            });
            if (response.data.status == 201) {
                setMessage("Cập nhật thông tin thành công!");
                setIsEditing(false);
                setUserData(response.data.data);
            } else {
                setMessage("Cập nhật thông tin thất bại.");
            }
        } catch (error) {
            console.error("Lỗi khi cập nhật thông tin:", error);
            setMessage(error.response?.data?.message || "Đã xảy ra lỗi.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <main className="flex min-h-screen bg-gray-50">
            <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
                <h1 className="text-2xl font-bold mb-6">Profile</h1>
                {/* Phần còn lại của code giữ nguyên */}
                <div className="flex flex-row justify-between items-center">
                    <div className="flex items-center space-x-4 p-4">
                    {hasAvatar ? (
                            <img
                                src={`https://ui-avatars.com/api/?background=c7d2fe&color=3730a3&bold=true&name=${userData.firstName}+${userData.lastName}`}
                                alt="User Avatar"
                                className="w-16 h-16 rounded-full object-cover border-2 border-gray-300"
                            />
                        ) : (
                            <div className="w-16 h-16 rounded-full bg-indigo-100 border-2 border-gray-300 flex items-center justify-center">
                                <span className="text-2xl font-bold text-indigo-800">
                                    {userInitials}
                                </span>
                            </div>
                        )}
                        <div>
                            <h2 className="text-xl font-semibold text-gray-900">
                                {userData.firstName} {userData.lastName}
                            </h2>
                            <p className="text-gray-500">{userData.email}</p>
                        </div>
                    </div>
                    <button
                        onClick={isEditing ? handleSave : () => setIsEditing(true)}
                        disabled={isLoading}
                        className={`bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center hover:bg-blue-600 ${isLoading ? "opacity-50 cursor-not-allowed" : ""}`}
                    >
                        {isLoading ? (
                            "Loading..."
                        ) : isEditing ? (
                            <>
                                <Check className="mr-2" /> <span className="hidden sm:inline">Save</span>
                            </>
                        ) : (
                            <>
                                <Pencil className="mr-2" /> <span className="hidden sm:inline">Edit</span>
                            </>
                        )}
                    </button>
                </div>
                {isLoading && !isEditing ? (
                    <div className="text-center">Đang tải thông tin...</div>
                ) : (
                    <form className="bg-white p-6 rounded-lg shadow-md grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div className="mb-4">
                            <label className="block font-medium mb-2">First Name</label>
                            <input
                                type="text"
                                value={userData.firstName || ""}
                                name="firstName"
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
                                value={userData.lastName || ""}
                                name="lastName"
                                onChange={handleChange}
                                readOnly={!isEditing}
                                disabled={!isEditing}
                                className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`}
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block font-medium mb-2">Username</label>
                            <input
                                type="text"
                                value={userData.username || ""}
                                name="username"
                                onChange={handleChange}
                                readOnly={!isEditing}
                                disabled={!isEditing}
                                className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`}
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block font-medium mb-2">Email</label>
                            <input
                                type="text"
                                value={userData.email || ""}
                                name="email"
                                readOnly
                                disabled
                                className="w-full px-3 py-2 border rounded-lg bg-gray-100 cursor-default"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block font-medium mb-2">Phone Number</label>
                            <input
                                type="text"
                                value={userData.phone || ""}
                                name="phone"
                                onChange={handleChange}
                                readOnly
                                disabled
                                className="w-full px-3 py-2 border rounded-lg bg-gray-100 cursor-default"
                                
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block font-medium mb-2">Address</label>
                            <input
                                type="text"
                                value={userData.address || ""}
                                name="address"
                                onChange={handleChange}
                                readOnly={!isEditing}
                                disabled={!isEditing}
                                className={`w-full px-3 py-2 border rounded-lg ${isEditing ? "bg-white" : "bg-gray-100 cursor-default"}`}
                            />
                        </div>
                    </form>
                )}
                {message && (
                    <div
                        className={`mt-4 p-4 rounded-lg ${message.includes("thành công") ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"}`}
                    >
                        {message}
                    </div>
                )}
            </div>
        </main>
    );
}