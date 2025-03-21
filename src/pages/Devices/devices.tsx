import React, { useState, useEffect } from "react";
import { SwitchToggle } from "../../components/common/Switch.tsx";
import { Lamp, Microwave, RadioReceiver, MonitorSpeaker, LucideProps } from "lucide-react";
import axios from "axios";
import { useLocation } from "react-router-dom";

interface Relay {
    relayName: string;
    title: string;
    status: string;
    icon: React.ForwardRefExoticComponent<Omit<LucideProps, "ref"> & React.RefAttributes<SVGSVGElement>>;
}

const DeviceCard = ({ title, icon: Icon, relayName, email, status }: Relay & { email: string | null }) => {
    const [isOn, setIsOn] = useState(status === "ON");
    const [error, setError] = useState("");

    useEffect(() => {
        setIsOn(status === "ON"); // Cập nhật trạng thái từ props
    }, [status]);

    const handleToggle = async () => {
        const newStatus = isOn ? "OFF" : "ON";
        try {
            console.log("Updating relay:", { email_user: email, relayName, status: newStatus });
            const response = await axios.post(
                "http://192.168.1.12:8000/api/relay/update",
                { email_user: email, relayName, status: newStatus },
                { headers: { "Content-Type": "application/json" } }
            );
            console.log("Update response:", response.data);
            setIsOn(newStatus === "ON");
            setError("");
        } catch (error) {
            console.error(`Error updating ${relayName}:`, error.response?.status, error.response?.data || error.message);
            setError(error.response?.data?.message || "Không thể cập nhật relay.");
        }
    };

    return (
        <div className="bg-gradient-to-br from-white to-gray-50 rounded-xl p-2 sm:p-4 lg:p-6 shadow-lg border border-gray-100">
            <div className="flex items-center gap-2 justify-between">
                <div className="flex flex-col items-center">
                    <div className="p-1 sm:p-2 lg:p-3 bg-blue-50 rounded-lg">
                        <Icon className="text-blue-500 w-4 h-4 sm:w-5 sm:h-5 lg:w-6 lg:h-6" />
                    </div>
                    <p className="text-gray-500 text-xs sm:text-sm font-medium pt-1">{title}</p>
                </div>
                <SwitchToggle checked={isOn} onChange={handleToggle} />
            </div>
            {error && <p className="text-red-500 text-xs mt-2">{error}</p>}
        </div>
    );
};

const Devices: React.FC = () => {
    const [relays, setRelays] = useState<Relay[]>([]);
    const [userEmail, setUserEmail] = useState(localStorage.getItem("userEmail") );
    const [errorMessage, setErrorMessage] = useState("");
    const location = useLocation();

    const relayNames = ["nutnhan_1", "nutnhan_2", "nutnhan_3", "nutnhan_4"];
    const relayIcons = [Lamp, RadioReceiver, MonitorSpeaker, Microwave];

    // Hàm lấy trạng thái ban đầu
    const fetchRelayStatus = async () => {
        if (!userEmail) {
            setErrorMessage("Vui lòng đăng nhập để xem trạng thái relay.");
            return;
        }

        try {
            const response = await axios.get(
                "http://192.168.1.12:8000/api/relay/getAllStatus",
                {
                    params: { email_user: userEmail },
                    headers: { "Content-Type": "application/json" },
                }
            );

            console.log("API Response:", response.data);
            const relayData = response.data.data || {};
            const updatedRelays = relayNames.map((relayName, index) => ({
                relayName,
                title: `Relay ${index + 1}`,
                status: relayData[relayName]?.status || "OFF",
                icon: relayIcons[index % relayIcons.length],
            }));

            setRelays(updatedRelays);
            setErrorMessage("");
        } catch (error) {
            console.error("Error fetching relay statuses:", error);
            setErrorMessage("Không thể tải trạng thái relay.");
            const defaultRelays = relayNames.map((relayName, index) => ({
                relayName,
                title: `Relay ${index + 1}`,
                status: "OFF",
                icon: relayIcons[index % relayIcons.length],
            }));
            setRelays(defaultRelays);
        }
    };

    // Kết nối WebSocket để nhận cập nhật real-time
    useEffect(() => {
        fetchRelayStatus(); // Lấy trạng thái ban đầu
    
        // Dùng ws:// cho local, wss:// cho production (Render)
        const wsUrl = window.location.hostname === "localhost" || window.location.hostname === "192.168.1.12"
            ? "ws://192.168.1.12:8000/ws/relay"
            : "wss://do-an-da-nganh.onrender.com/ws/relay";
        const ws = new WebSocket(wsUrl);
    
        ws.onopen = () => {
            console.log("WebSocket connected");
        };
    
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log("WebSocket message received:", message);
            const relayData = message.data || {};
            const updatedRelays = relayNames.map((relayName, index) => ({
                relayName,
                title: `Relay ${index + 1}`,
                status: relayData[relayName]?.status || "OFF",
                icon: relayIcons[index % relayIcons.length],
            }));
            setRelays(updatedRelays);
        };
    
        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };
    
        ws.onclose = () => {
            console.log("WebSocket disconnected");
        };
    
        return () => {
            ws.close();
        };
    }, [userEmail]);

    const handleDeleteRelay = async (relayName: string) => {
        try {
            await axios.delete("http://192.168.1.12:8000/api/relay/delete", {
                headers: { "Content-Type": "application/json" },
                data: { email_user: userEmail, relayName },
            });
            setRelays((prev) => prev.filter((relay) => relay.relayName !== relayName));
        } catch (error) {
            console.error(`Error deleting ${relayName}:`, error.response?.status, error.response?.data);
        }
    };

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
                                            <th className="px-2 sm:px-4 py-2 text-left">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody className="text-sm">
                                        {relays.map((relay, index) => (
                                            <tr key={index} className="border-t">
                                                <td className="px-2 sm:px-4 py-2">{relay.title}</td>
                                                <td className="px-2 sm:px-4 py-2">{relay.status}</td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">{userEmail}</td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">-</td>
                                                <td className="px-2 sm:px-4 py-2 sm:table-cell">-</td>
                                                <td className="px-2 sm:px-4 py-2">
                                                    <button
                                                        onClick={() => handleDeleteRelay(relay.relayName)}
                                                        className="text-red-500 hover:underline"
                                                    >
                                                        Delete
                                                    </button>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <div className="bg-slate-200 rounded-lg col-span-1">
                        <form className="bg-white max-h-64 p-6 rounded-lg shadow-md">
                            <div className="mb-4">
                                <label className="block font-medium mb-2 text-sm sm:text-base">Start Time</label>
                                <input type="datetime-local" className="w-full px-2 sm:px-3 py-1 sm:py-2 border rounded-lg text-sm" />
                            </div>
                            <div className="mb-4">
                                <label className="block font-medium mb-2 text-sm sm:text-base">End Time</label>
                                <input type="datetime-local" className="w-full px-2 sm:px-3 py-1 sm:py-2 border rounded-lg text-sm" />
                            </div>
                            <div className="flex justify-end gap-2 sm:gap-4">
                                <button type="submit" className="px-3 sm:px-4 py-1 sm:py-2 bg-indigo-500 text-white rounded-lg">
                                    Save
                                </button>
                                <button type="reset" className="px-3 sm:px-4 py-1 sm:py-2 bg-gray-200 text-gray-700 rounded-lg">
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </main>
    );
};

export default Devices;