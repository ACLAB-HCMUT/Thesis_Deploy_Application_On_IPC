import React, { createContext, useContext, useState, useEffect, useRef } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { ChevronFirst, ChevronLast, MoreVertical } from 'lucide-react';
import NotificationBellIcon from "../ui/NotificationBellIcon.tsx";
import Header from "../../components/common/Header.tsx";
import axios from "axios";

const SidebarContext = createContext({ isExpanded: true });

const getInitials = (firstName, lastName) => {
    const firstInitial = firstName?.charAt(0)?.toUpperCase() || '';
    const lastInitial = lastName?.charAt(0)?.toUpperCase() || '';
    return `${firstInitial}${lastInitial}`;
};

const Logo = require("../../assets/image/logo.png");

export default function Sidebar({ children }) {
    const [message, setMessage] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [isExpanded, setIsExpanded] = useState(false);
    const [userData, setUserData] = useState({
        firstName: "",
        lastName: "",
        username: "",
        email: "",
        phone: "",
        address: "",
    });
    const [showProfileMenu, setShowProfileMenu] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();
    const sidebarRef = useRef<HTMLDivElement>(null);
    
    // Unified notification state
    const [unreadNotifications, setUnreadNotifications] = useState(0);
    
    // Single event listener for notification updates
    useEffect(() => {
        const handleNotificationUpdate = (e: Event) => {
            // Chuyển đổi kiểu an toàn
            const event = e as CustomEvent<{unreadCount: number}>;
            console.log("Notification update received:", event.detail);
            if (event.detail && typeof event.detail.unreadCount === 'number') {
                setUnreadNotifications(event.detail.unreadCount);
            }
        };
        
        window.addEventListener('notificationUpdate', handleNotificationUpdate);
        return () => {
            window.removeEventListener('notificationUpdate', handleNotificationUpdate);
        };
    }, []);

    useEffect(() => {
        const fetchUserData = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get("http://localhost:8000/api/users/info", {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("access_token")}`,
                    },
                });
                console.log("API Response:", response.data);
                if (response.data.status == 201) {
                    setUserData(response.data.data);
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
    
    // Add global click event to collapse sidebar when clicking outside on small screens
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            // Only apply on small screens (< 1024px)
            if (isExpanded && sidebarRef.current) {
                // Check if click is outside the sidebar
                if (!sidebarRef.current.contains(event.target as Node)) {
                    setIsExpanded(false);
                }
            }
        };

        // Attach click event to document
        document.addEventListener("mousedown", handleClickOutside);

        // Clean up event when component unmounts
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isExpanded]);
    
    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('userEmail');
        localStorage.removeItem('persist:root');
        navigate('/login');
        setShowProfileMenu(false);
    };

    const userInitials = getInitials(userData.firstName, userData.lastName);
    const toggleSidebar = () => setIsExpanded((prev) => !prev);

    return (
        <div>
            <Header toggleSidebar={toggleSidebar} />
            <aside className="h-screen">
                <nav ref={sidebarRef}
                 className={`fixed top-0 left-0 z-40 pt-20 h-full flex flex-col bg-white border-r shadow-sm lg:translate-x-0 transition-transform ${isExpanded ? "translate-x-0" : "-translate-x-full"}`}>
                    <SidebarContext.Provider value={{ isExpanded }}>
                    <ul className="flex-1 px-3">
                        {React.Children.map(children, (child) => {
                            // Check if this is the notification item
                            const isNotificationItem = child.props.text && 
                                (child.props.text.toLowerCase() === "notifications" || 
                                 child.props.text.toLowerCase() === "thông báo");
                            
                            // For notification item, apply special styling with NotificationBellIcon
                            if (isNotificationItem) {
                                return React.cloneElement(child, {
                                    active: child.props.to === location.pathname,
                                    unreadCount: unreadNotifications,
                                    icon: <NotificationBellIcon unreadCount={unreadNotifications} />,
                                });
                            }
                            
                            // For other items, keep unchanged
                            return React.cloneElement(child, {
                                active: child.props.to === location.pathname,
                            });
                        })}
                    </ul>
                    </SidebarContext.Provider>

                    {/* Profile section with dropdown */}
                    <div className="border-t flex p-3 relative">
                        <div
                            className="flex items-center cursor-pointer"
                            onClick={() => setShowProfileMenu(!showProfileMenu)}
                        >
                            <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center border border-gray-300">
                                <span className="text-lg font-semibold text-indigo-800">
                                    {userInitials || "U"}
                                </span>
                            </div>
                            <div className={`flex justify-between items-center overflow-hidden transition-all ${isExpanded ? "w-52 ml-3" : "w-0"}`}>
                                <div className="leading-4">
                                    <h4 className="font-semibold">{userData.firstName} {userData.lastName}</h4>
                                    <span className="text-xs text-gray-600">{userData.email}</span>
                                </div>
                                <MoreVertical size={20} />
                            </div>
                        </div>

                        {showProfileMenu && (
                            <div className="absolute bottom-full left-0 mb-2 w-48 bg-white rounded-md shadow-lg border border-gray-100">
                                <Link
                                    to="/profile"
                                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                    onClick={() => setShowProfileMenu(false)}
                                >
                                    Profile
                                </Link>
                                <button
                                    onClick={handleLogout}
                                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                                >
                                    Logout
                                </button>
                            </div>
                        )}
                    </div>
                </nav>
            </aside>
        </div>
    );
}

export function SidebarItem({ icon, text, active, alert, to, unreadCount = 0 }) {
    const { isExpanded } = useContext(SidebarContext);
    const navigate = useNavigate();

    const handleClick = () => {
        if (to) {
            navigate(to);
        }
    };
    
    // Ensure hasUnread is always true when there are unread notifications
    const hasUnread = unreadCount > 0;
    
    // Debug log for notification items
    if (text === "Notifications" || text === "Thông báo") {
        console.log(`SidebarItem "${text}" rendering with unreadCount: ${unreadCount}, hasUnread: ${hasUnread}`);
    }

    const isNotificationItem = text && 
        (text.toLowerCase() === "notifications" || 
         text.toLowerCase() === "thông báo");

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
          {/* Wrapper for the icon with special treatment for notification icon */}
          <div className="relative">
            {icon}
          </div>
          
          <span className={`overflow-hidden transition-all ${isExpanded ? "w-52 ml-3" : "w-0"}`}>
            {text}
            {isNotificationItem && hasUnread && (
              <span className="ml-2 bg-red-500 text-white text-xs px-1.5 py-0.5 rounded-full">
                {unreadCount}
              </span>
            )}
          </span>
          
          {alert && (
            <div className={`absolute right-2 w-2 h-2 rounded bg-indigo-400 ${isExpanded ? "" : "top-2"}`} />
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
              {isNotificationItem && hasUnread && (
                <span className="ml-1 bg-red-500 text-white text-xs px-1.5 py-0.5 rounded-full">
                  {unreadCount <= 99 ? unreadCount : "99+"}
                </span>
              )}
            </div>
          )}
        </li>
    );
}