import { Outlet } from 'react-router-dom';


function App() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-grow">
        <Outlet />
      </main>
    </div>
  );
}

export default App;
