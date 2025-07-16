import { useLocation } from "react-router-dom";

export default function useIsKanbanRoute() {
  const location = useLocation();
  return location.pathname === "/kanban";
}
