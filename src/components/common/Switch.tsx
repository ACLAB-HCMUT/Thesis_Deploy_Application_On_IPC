import React from "react";

// Định nghĩa interface cho props
interface SwitchToggleProps {
    checked: boolean; // Trạng thái bật/tắt
    onChange: () => void; // Hàm gọi khi toggle thay đổi
}

export function SwitchToggle({ checked, onChange }: SwitchToggleProps) {
    return (
        <div
            className={`flex items-center space-x-2 p-2 rounded-full transition-colors cursor-pointer`}
            onClick={onChange} // Gọi onChange khi click
        >
            <div
                className={`w-20 h-10 flex items-center bg-gray-300 rounded-full p-1 duration-300 ease-in-out shadow-md ${
                    checked ? "bg-green-400" : "bg-gray-400"
                }`}
            >
                <div
                    className={`w-8 h-8 rounded-full transition-transform transform ${
                        checked ? "bg-green-700 translate-x-9" : "bg-gray-600 translate-x-0"
                    }`}
                />
            </div>
            <span className={`font-medium ${checked ? "text-green-600" : "text-gray-500"}`}>
                {checked ? "ON" : "OFF"}
            </span>
        </div>
    );
}