import React, { useState, useEffect } from "react";
import { SwitchToggle } from "../../components/common/Switch.tsx";
import { Lamp, Microwave, RadioReceiver, MonitorSpeaker, LucideProps, X, History } from "lucide-react";
import axios from "axios";
import { useLocation } from "react-router-dom";

interface Relay {
    relayName: string;
    title: string;
    status: string;
    updatedBy?: string;
    icon: React.ForwardRefExoticComponent<Omit<LucideProps, "ref"> & React.RefAttributes<SVGSVGElement>>;
    timeStart?: string;
    timeEnd?: string;
    schedulerId?: string;
    repeatDaily?: boolean;
    schedulerUser?: string;
    schedulers?: any[];
}
interface RelayHistory {
    _id?: string;
    relayName: string;
    status: string;
    timestamp: string;
    email_user?: string;
}

// Hàm định dạng thời gian theo yêu cầu: HH:MM, dd/MM/yyyy
const formatDateTime = (dateTimeString?: string) => {
    if (!dateTimeString) return "-";
    
    const date = new Date(dateTimeString);
    return date.toLocaleString('vi-VN', {
        hour: '2-digit',
        minute: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
};

// Hàm định dạng thời gian chỉ giờ phút: HH:MM// Hàm định dạng thời gian chỉ giờ phút: HH:MM
const formatTime = (dateTimeString?: string) => {
    if (!dateTimeString) return "-";
    
    // Create a date object (JavaScript will convert to local time internally)
    const date = new Date(dateTimeString);
    
    // Format hours and minutes without timezone conversion
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `${hours}:${minutes}`;
};

const DeviceCard = ({ title, icon: Icon, relayName, email, status, relayObj}: { title: string, icon: any, relayName: string, email: string | null, status: string, relayObj: Relay }) => {
    const [isOn, setIsOn] = useState(status === "ON");
    const [error, setError] = useState("");
    const [historyPopup, setHistoryPopup] = useState(false);
    const [relayHistory, setRelayHistory] = useState<RelayHistory[]>([]);
    const token = localStorage.getItem("access_token");
    
    useEffect(() => {
        setIsOn(status === "ON");
        
    }, [status]);

    const handleToggle = async () => {
        const newStatus = isOn ? "OFF" : "ON";
        try {
            const response = await axios.post(
                "http://localhost:8000/api/relay/update",
                { email_user: email, relayName, status: newStatus },
                { headers: { "Content-Type": "application/json" } }
            );
            console.log("Update response:", response.data);
            setIsOn(newStatus === "ON");
            
            setError("");
            
        } catch (error) {
            setError(error.response?.data?.message || "Không thể cập nhật relay.");
        }
    };

    const fetchRelayHistory = async () => {
        if (!token) {
            setError("Không tìm thấy token. Vui lòng đăng nhập lại.");
            return;
        }

        try {
            const response = await axios.post(
                "http://localhost:8000/api/relay/getHistory",
                { relayName },
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                }
            );
            const historyData = response.data.data || [];
            setRelayHistory(historyData);
            setHistoryPopup(true);
            setError("");
        } catch (error) {
            setError(error.response?.data?.message || "Không thể tải lịch sử relay.");
        }
    };

    const handleDeleteHistory = async (historyId: string) => {
        if (!window.confirm("Bạn có chắc chắn muốn xóa bản ghi lịch sử này không?")) {
            return;
        }
        if (!token) {
            setError("Không tìm thấy token. Vui lòng đăng nhập lại.");
            return;
        }

        try {
            const response = await axios.post(
                "http://localhost:8000/api/relay/deleteHistory",
                { history_id: historyId },
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                }
            );
            if (response.data.status === 200) {
                setRelayHistory((prev) => prev.filter((entry) => entry._id !== historyId));
                setError("");
            }
        } catch (error) {
            setError(error.response?.data?.message || "Không thể xóa lịch sử relay.");
        }
    };

    const handleDeleteAllHistory = async () => {
        if (!window.confirm("Bạn có chắc chắn muốn xóa toàn bộ lịch sử không?")) {
            return;
        }
        if (!token) {
            setError("Không tìm thấy token. Vui lòng đăng nhập lại.");
            return;
        }

        try {
            const response = await axios.post(
                "http://localhost:8000/api/relay/deleteAllHistory",
                { relayName },
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                }
            );
            if (response.data.status === 200) {
                setRelayHistory([]);
                setError("");
            }
        } catch (error) {
            setError(error.response?.data?.message || "Không thể xóa toàn bộ lịch sử relay.");
        }
    };

    return (
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl p-2 sm:p-4 lg:p-6 shadow-lg border border-gray-100 relative">
            <div className="flex items-center gap-2 justify-between">
                <div className="flex flex-col items-center">
                    <div className="p-1 sm:p-2 lg:p-3 bg-blue-50 rounded-lg">
                        <Icon className="text-blue-500 w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6" />
                    </div>
                    <p className="text-gray-500 text-xs sm:text-sm font-medium pt-1">{title}</p>
                </div>
                <SwitchToggle checked={isOn} onChange={handleToggle} />
            </div>
            
            {relayObj.timeStart && relayObj.timeEnd && (
                <div className="mt-2 text-xs text-gray-600">
                    <p>Schedule: {formatTime(relayObj.timeStart)} - {formatTime(relayObj.timeEnd)}</p>
                    <p>Repeat: {relayObj.repeatDaily ? "Daily" : "No"}</p>
                </div>
            )}
            
            <button 
                onClick={fetchRelayHistory} 
                className="absolute bottom-2 right-2 text-blue-500 hover:text-blue-700 flex items-center text-xs"
            >
                <History className="w-3 h-3 mr-1" />
                History
            </button>
            
            {error && <p className="text-red-500 text-xs mt-2">{error}</p>}
            
            {historyPopup && (
                <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[90vw] sm:max-w-lg">
                        <h2 className="text-lg sm:text-xl font-bold mb-4">Lịch sử {title}</h2>
                        <div className="max-h-64 overflow-y-auto">
                            {relayHistory.length === 0 ? (
                                <table className="w-full text-xs sm:text-sm min-w-[500px]">
                                    <thead>
                                        <tr className="bg-gray-100">
                                            <th className="px-2 sm:px-4 py-2 text-left">Status</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">Time</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">User</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            <td colSpan={4} className="px-2 sm:px-4 py-2 text-center text-gray-500">
                                                Không có lịch sử nào để hiển thị.
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            ) : (
                                <div className="overflow-x-auto">
                                    <table className="w-full text-xs sm:text-sm min-w-[500px]">
                                        <thead>
                                            <tr className="bg-gray-100">
                                                <th className="px-2 sm:px-4 py-2 text-left">Status</th>
                                                <th className="px-2 sm:px-4 py-2 text-left">Time</th>
                                                <th className="px-2 sm:px-4 py-2 text-left">User</th>
                                                <th className="px-2 sm:px-4 py-2 text-left">Action</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {relayHistory.map((entry, index) => (
                                                <tr key={index} className="border-t">
                                                    <td className="px-2 sm:px-4 py-2">{entry.status}</td>
                                                    <td className="px-2 sm:px-4 py-2">{formatDateTime(entry.timestamp)}</td>
                                                    <td className="px-2 sm:px-4 py-2">{entry.email_user || "Unknown"}</td>
                                                    <td className="px-2 sm:px-4 py-2">
                                                        <button
                                                            onClick={() => entry._id && handleDeleteHistory(entry._id)}
                                                            className="text-red-500 hover:text-red-700"
                                                        >
                                                            <X className="w-4 h-4" />
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            )}
                        </div>
                        <div className="mt-4 flex justify-between">
                            <button
                                onClick={handleDeleteAllHistory}
                                className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 text-sm sm:text-base"
                            >
                                Delete All
                            </button>
                            <button
                                onClick={() => setHistoryPopup(false)}
                                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 text-sm sm:text-base"
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
const Devices: React.FC = () => {
    const [relays, setRelays] = useState<Relay[]>([]);
    const [userEmail, setUserEmail] = useState(localStorage.getItem("userEmail"));
    const [errorMessage, setErrorMessage] = useState("");
    const [selectedRelay, setSelectedRelay] = useState("");
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");
    const [repeatDaily, setRepeatDaily] = useState(false);
    const [schedulerHistory, setSchedulerHistory] = useState<any[]>([]);
    const [historyPopup, setHistoryPopup] = useState(false);
    const [currentRelay, setCurrentRelay] = useState("");
    const location = useLocation();

    const relayNames = ["nutnhan1", "nutnhan2", "nutnhan3", "nutnhan4"];
    const relayIcons = [Lamp, RadioReceiver, MonitorSpeaker, Microwave];
    const token = localStorage.getItem("access_token");

    const fetchRelayStatus = async () => {
        if (!userEmail || !token) {
            setErrorMessage("Vui lòng đăng nhập lại.");
            return;
        }

        try {
            const [relayResponse, schedulerResponse] = await Promise.all([
                axios.get("http://localhost:8000/api/relay/getAllStatus", {
                    params: { email_user: userEmail },
                    headers: { "Content-Type": "application/json" },
                }),
                axios.get("http://localhost:8000/api/setup/scheduler", {
                    headers: { 
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}` 
                    },
                }).catch(err => {
                    console.error("Scheduler API error:", err.response || err);
                    return { data: { data: [] } };
                })
            ]);
            console.log(relayResponse.data.data, "aaa");
            const relayData = relayResponse.data.data || {};
            const schedulerData = schedulerResponse.data.data || [];

            const updatedRelays = relayNames.map((relayName, index) => {
                const relaySchedulers = schedulerData.filter(s => s.relayName === relayName);
                const firstScheduler = relaySchedulers[0] || {};
                return {
                    relayName,
                    title: `Relay ${index + 1}`,
                    status: relayData[relayName]?.status || "OFF",
                    updatedBy: relayData[relayName]?.updated_by || "Unknown",
                    icon: relayIcons[index % relayIcons.length],
                    timeStart: firstScheduler.timeStart ? new Date(firstScheduler.timeStart).toISOString() : undefined,
                    timeEnd: firstScheduler.timeEnd ? new Date(firstScheduler.timeEnd).toISOString() : undefined,
                    schedulerId: firstScheduler.id,
                    repeatDaily: firstScheduler.repeatDaily || false,
                    schedulerUser: firstScheduler.email || "Unknown",
                    schedulers: relaySchedulers
                };
            });
            setRelays(updatedRelays);
            setErrorMessage("");
        } catch (error) {
            setErrorMessage(error.response?.data?.message || "Không thể tải dữ liệu.");
        }
    };

    const handleSchedulerSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!selectedRelay || !startTime || !endTime) {
            setErrorMessage("Vui lòng điền đầy đủ thông tin");
            return;
        }
        if (!token) {
            setErrorMessage("Không tìm thấy token. Vui lòng đăng nhập lại.");
            return;
        }
        
        const today = new Date();
        const [startHours, startMinutes] = startTime.split(':').map(Number);
        const [endHours, endMinutes] = endTime.split(':').map(Number);
        
        const startDate = new Date(today.getFullYear(), today.getMonth(), today.getDate(), startHours, startMinutes, 0);
        const endDate = new Date(today.getFullYear(), today.getMonth(), today.getDate(), endHours, endMinutes, 0);
        
        const formatDateWithoutOffset = (date: Date) => {
            const pad = (num: number) => String(num).padStart(2, '0');
            return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T` +
                   `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
        };
    
        if (endDate <= startDate) {
            setErrorMessage("Thời gian kết thúc phải sau thời gian bắt đầu.");
            return;
        }
    
        // Log giá trị trước khi gửi API
        const payload = {
            email: userEmail,
            relayName: selectedRelay,
            timeStart: formatDateWithoutOffset(startDate),
            timeEnd: formatDateWithoutOffset(endDate),
            repeatDaily: repeatDaily
        };
        console.log("Dữ liệu gửi lên API:", payload);
    
        try {
            const response = await axios.post(
                "http://localhost:8000/api/setup/scheduler",
                payload,
                {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    }
                }
            );
        
            if (response.data) {
                alert("Tạo lịch hẹn thành công!");
                await fetchRelayStatus();
                setStartTime("");
                setEndTime("");
                setSelectedRelay("");
                setRepeatDaily(false);
                setErrorMessage("");
            }
        } catch (error) {
            if (error.response?.status === 409) {
                const conflict = error.response.data.data.conflicting_schedule;
                const recommendation = error.response.data.data.recommendation;
                setErrorMessage(
                    `Lịch hẹn từ ${formatTime(startDate.toISOString())} đến ${formatTime(endDate.toISOString())} ` +
                    `trùng với lịch hiện có từ ${formatTime(conflict.timeStart)} đến ${formatTime(conflict.timeEnd)}. ` +
                    `${recommendation}`
                );
            } else {
                setErrorMessage(error.response?.data?.message || "Không thể tạo lịch hẹn.");
            }
        }
    };
    const fetchSchedulerHistory = async (relayName: string) => {
        const relay = relays.find(r => r.relayName === relayName);
        if (relay && relay.schedulers) {
            setSchedulerHistory(relay.schedulers);
            setCurrentRelay(relayName);
            setHistoryPopup(true);
            setErrorMessage("");
        }
    };

    const handleDeleteScheduler = async (schedulerId: string) => {
        if (!window.confirm("Bạn có chắc chắn muốn xóa scheduler này không?")) {
            return;
        }
        if (!token) {
            setErrorMessage("Không tìm thấy token. Vui lòng đăng nhập lại.");
            return;
        }

        try {
            await axios.delete("http://localhost:8000/api/setup/scheduler", {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                data: { id: schedulerId }
            });
            setSchedulerHistory(prev => prev.filter(s => s.id !== schedulerId));
            await fetchRelayStatus();
        } catch (error) {
            setErrorMessage(error.response?.data?.message || "Không thể xóa scheduler.");
        }
    };

    const handleDeleteAllSchedulers = async () => {
        if (!window.confirm("Bạn có chắc chắn muốn xóa toàn bộ scheduler không?")) {
            return;
        }
        if (!token) {
            setErrorMessage("Không tìm thấy token. Vui lòng đăng nhập lại.");
            return;
        }

        try {
            const schedulersToDelete = schedulerHistory.map(s => s.id);
            await Promise.all(schedulersToDelete.map(id =>
                axios.delete("http://localhost:8000/api/setup/scheduler", {
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    data: { id }
                })
            ));
            setSchedulerHistory([]);
            await fetchRelayStatus();
        } catch (error) {
            setErrorMessage(error.response?.data?.message || "Không thể xóa toàn bộ scheduler.");
        }
    };

    const renderSchedulerHistoryPopup = () => (
        historyPopup && (
            <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-4 sm:p-6 w-full max-w-[90vw] sm:max-w-lg">
                    <h2 className="text-lg sm:text-xl font-bold mb-4">Lịch sử Scheduler - {relays.find(r => r.relayName === currentRelay)?.title}</h2>
                    <div className="max-h-64 overflow-y-auto">
                        {schedulerHistory.length === 0 ? (
                            <table className="w-full text-xs sm:text-sm min-w-[500px]">
                                <thead>
                                    <tr className="bg-gray-100">
                                        <th className="px-2 sm:px-4 py-2 text-left">Start Time</th>
                                        <th className="px-2 sm:px-4 py-2 text-left">End Time</th>
                                        <th className="px-2 sm:px-4 py-2 text-left">Daily Repeat</th>
                                        <th className="px-2 sm:px-4 py-2 text-left">Created At</th>
                                        <th className="px-2 sm:px-4 py-2 text-left">Action</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colSpan={5} className="px-2 sm:px-4 py-2 text-center text-gray-500">
                                            Không có lịch sử scheduler nào để hiển thị.
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        ) : (
                            <div className="overflow-x-auto">
                                <table className="w-full text-xs sm:text-sm min-w-[500px]">
                                    <thead>
                                        <tr className="bg-gray-100">
                                            <th className="px-2 sm:px-4 py-2 text-left">Start Time</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">End Time</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">Daily Repeat</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">Created At</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {schedulerHistory.map((scheduler, index) => (
                                            <tr key={index} className="border-t">
                                                <td className="px-2 sm:px-4 py-2">{formatTime(scheduler.timeStart)}</td>
                                                <td className="px-2 sm:px-4 py-2">{formatTime(scheduler.timeEnd)}</td>
                                                <td className="px-2 sm:px-4 py-2">{scheduler.repeatDaily ? "Yes" : "No"}</td>
                                                <td className="px-2 sm:px-4 py-2">{formatDateTime(scheduler.timestamp)}</td>
                                                <td className="px-2 sm:px-4 py-2">
                                                    <button
                                                        onClick={() => handleDeleteScheduler(scheduler.id)}
                                                        className="text-red-500 hover:text-red-700"
                                                    >
                                                        <X className="w-4 h-4" />
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        )}
                    </div>
                    <div className="mt-4 flex justify-between">
                        <button
                            onClick={handleDeleteAllSchedulers}
                            className="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 text-sm sm:text-base"
                        >
                            Delete All
                        </button>
                        <button
                            onClick={() => setHistoryPopup(false)}
                            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 text-sm sm:text-base"
                        >
                            Close
                        </button>
                    </div>
                </div>
            </div>
        )
    );
    
    useEffect(() => {
        fetchRelayStatus();
        const ws = new WebSocket("ws://localhost:8000/ws/relay");
        ws.onopen = () => {
            console.log("WebSocket connected");
        };
        ws.onmessage = (event) => {
            console.log("WebSocket message received:", event.data);
            const message = JSON.parse(event.data);
            
            const relayData = message.data || {};
            console.log("Relay data:", relayData);
            setRelays(prev => prev.map(relay => ({
                ...relay,
                status: relayData[relay.relayName]?.status || relay.status,
                updatedBy: relayData[relay.relayName]?.updated_by || relay.updatedBy
            })));
        };
        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };

        ws.onclose = () => {
            console.log("WebSocket closed");
            // Có thể thử kết nối lại sau một khoảng thời gian
            setTimeout(() => {
              // Logic reconnect nếu cần
            }, 1000);
          };
        return () => ws.close();
    }, [userEmail]);

    return (
        <main className="flex min-h-screen bg-gray-50">
            <div className="flex-1 mt-16 p-4 space-y-6 sm:space-y-8 ml-0 lg:ml-16">
                <h1 className="text-2xl font-bold mb-6">Devices</h1>
                {errorMessage && <p className="text-red-500 mb-4">{errorMessage}</p>}
                
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 xl:grid-cols-4 gap-3 sm:gap-4 lg:gap-6">
                    {relays.map((relay) => (
                        <DeviceCard
                            key={relay.relayName}
                            title={relay.title}
                            icon={relay.icon}
                            relayName={relay.relayName}
                            email={userEmail}
                            status={relay.status}
                            relayObj={relay}
                            
                        />
                    ))}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mt-5">
                    <div className="rounded-lg col-span-1 md:col-span-1 lg:col-span-3">
                        <div className="w-full bg-white rounded-lg shadow-md overflow-hidden">
                            <div className="max-h-96 overflow-y-auto">
                                <table className="w-full table-auto text-xs sm:text-sm">
                                    <thead className="text-xs text-gray-700 uppercase bg-gray-100 sticky top-0">
                                        <tr>
                                            <th className="px-2 sm:px-4 py-2 text-left">Device</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">Status</th>
                                            <th className="px-2 sm:px-4 py-2 text-left sm:table-cell">User</th>
                                            <th className="px-2 sm:px-4 py-2 text-left md:table-cell">Start Time</th>
                                            <th className="px-2 sm:px-4 py-2 text-left md:table-cell">End Time</th>
                                            <th className="px-2 sm:px-4 py-2 text-left md:table-cell">Daily Repeat</th>
                                            <th className="px-2 sm:px-4 py-2 text-left">History</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-sm">
                                        {relays.map((relay, index) => (
                                            <tr key={index} className="border-t">
                                                <td className="px-2 sm:px-4 py-2">{relay.title}</td>
                                                <td className="px-2 sm:px-4 py-2">{relay.status}</td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">
                                                    {relay.updatedBy}
                                                </td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">
                                                    {relay.timeStart ? formatTime(relay.timeStart) : "-"}
                                                </td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">
                                                    {relay.timeEnd ? formatTime(relay.timeEnd) : "-"}
                                                </td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">
                                                    {relay.repeatDaily ? "Yes" : "No"}  
                                                </td>
                                                <td className="px-2 sm:px-4 py-2">
                                                    <button
                                                        onClick={() => fetchSchedulerHistory(relay.relayName)}
                                                        className="text-blue-500 hover:underline"
                                                    >
                                                        History
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div className="bg-white rounded-lg col-span-1 shadow-md">
                        <form onSubmit={handleSchedulerSubmit} className="p-4 sm:p-6 space-y-4">
                            <div>
                                <label className="block font-medium mb-1 text-sm sm:text-base text-gray-700">
                                    Select Relay
                                </label>
                                <select
                                    value={selectedRelay}
                                    onChange={(e) => setSelectedRelay(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                >
                                    <option value="">Choose a relay</option>
                                    {relays.map((relay) => (
                                        <option key={relay.relayName} value={relay.relayName}>
                                            {relay.title}
                                        </option>
                                    ))}
                                </select>
                            </div>
                            <div>
                                <label className="block font-medium mb-1 text-sm sm:text-base text-gray-700">
                                    Start Time
                                </label>
                                <input
                                    type="time"
                                    value={startTime}
                                    onChange={(e) => setStartTime(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div>
                                <label className="block font-medium mb-1 text-sm sm:text-base text-gray-700">
                                    End Time
                                </label>
                                <input
                                    type="time"
                                    value={endTime}
                                    onChange={(e) => setEndTime(e.target.value)}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                />
                            </div>
                            <div className="flex items-center">
                                <input
                                    type="checkbox"
                                    id="repeatDaily"
                                    checked={repeatDaily}
                                    onChange={(e) => setRepeatDaily(e.target.checked)}
                                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                                />
                                <label htmlFor="repeatDaily" className="ml-2 block text-sm text-gray-700">
                                    Repeat Daily
                                </label>
                            </div>
                            <div className="flex justify-end gap-3">
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm sm:text-base"
                                >
                                    Save
                                </button>
                                <button
                                    type="reset"
                                    onClick={() => {
                                        setSelectedRelay("");
                                        setStartTime("");
                                        setEndTime("");
                                        setRepeatDaily(false);
                                    }}
                                    className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-400 text-sm sm:text-base"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
            {renderSchedulerHistoryPopup()}
        </main>
    );
};

export default Devices;