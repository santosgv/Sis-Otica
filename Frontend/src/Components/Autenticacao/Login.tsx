import React, { useContext,useState, type FormEvent } from "react";
import api from   '../../utils/axiosConfig';
import { setTokens } from '../../utils/auth';


type LoginProps = {
    onLoginSuccess: () => void;
};



const Home: React.FC<LoginProps> = ({ onLoginSuccess }) => {
      const [credentials, setCredentials] = useState({
        username: '',
        password: '',
      });
      const [error, setError] = useState('');
      const [loading, setLoading] = useState(false);
      
    
    const handleChange = (e)  => {
    const { name, value } = e.target;
        setCredentials({ ...credentials, [name]: value });
      };
    

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!credentials.username.trim() || !credentials.password.trim()) {
            setError("Por favor, preencha todos os campos.");
            return;
        }
      if (!credentials.username || !credentials.password) {
        setError('Por favor, preencha todos os campos.');
        setLoading(false);
        return;
      }

              try {
          const response = await api.post('token/', credentials);

          // ✅ Salva os tokens de forma centralizada
          setTokens({
            access: response.data.access,
            refresh: response.data.refresh,
          });
          

          // Aqui você pode redirecionar o usuário ou atualizar o estado da aplicação
          console.log('Login bem-sucedido!', response.data);
          window.location.assign("/");
        
    
        } catch (err) {
          // Trata erros (ex.: credenciais inválidas)
          setError(
            
            err.response?.data?.detail || 'Erro ao fazer login. Verifique suas credenciais.'
          
          );
        } finally {
          setLoading(false);
        }

    };

    return (
        <>
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 via-blue-300 to-blue-500 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 relative overflow-hidden transition-colors">
            {/* Efeito de partículas de fundo */}
            <div className="absolute inset-0 pointer-events-none z-0">
                <div className="absolute top-1/4 left-1/3 w-72 h-72 bg-cyan-300 opacity-30 rounded-full blur-3xl animate-pulse dark:bg-cyan-900" />
                <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-blue-400 opacity-20 rounded-full blur-2xl animate-pulse-slow dark:bg-blue-900" />
            </div>
            <form
                method="POST"
                onSubmit={handleSubmit}
                className="relative z-10 bg-white/70 dark:bg-gray-900/80 backdrop-blur-xl shadow-2xl rounded-3xl px-10 py-8 w-full max-w-md border border-white/40 dark:border-gray-700 ring-1 ring-blue-200/60 dark:ring-gray-700/60
                transition-all duration-300 hover:scale-[1.03] hover:shadow-blue-200/60 group"
                noValidate  
            >
                <div className="mb-10 text-center">
                    <h1 className="text-4xl font-black bg-gradient-to-r from-blue-700 via-cyan-400 to-blue-700 bg-clip-text text-transparent drop-shadow-xl tracking-widest uppercase border-b-4 border-blue-400 dark:border-cyan-700 pb-3 animate-fade-in">
                        Login
                    </h1>
                </div>
                {error && (
                    <div className="mb-5 text-center text-red-600 dark:text-red-400 font-semibold animate-shake">
                        {error}
                    </div>
                )}
                <div className="mb-7">
                    <label
                        className="block text-gray-700 dark:text-gray-200 font-bold mb-2 tracking-wide"
                        htmlFor="username"
                    >
                        Usuário
                    </label>
                    <input
                        type="text"
                        id="username"
                        className="w-full px-5 py-3 rounded-xl border border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-4 focus:ring-cyan-300/60 dark:focus:ring-cyan-900/60 focus:border-cyan-400 dark:focus:border-cyan-700 bg-white/80 dark:bg-gray-800 shadow-inner transition-all duration-200 ease-in-out text-lg placeholder:text-gray-400 dark:placeholder:text-gray-500"
                        name="username"
                        placeholder="Digite seu usuário"
                    
                        onChange={handleChange}
                        autoComplete="username"
                        required
                        aria-required="true"
                        aria-describedby="username-error"
                    />
                </div>
                <div className="mb-10">
                    <label
                        className="block text-gray-700 dark:text-gray-200 font-bold mb-2 tracking-wide"
                        htmlFor="password"
                    >
                        Senha
                    </label>
                    <input
                        type="password"
                        id="password"
                        className="w-full px-5 py-3 rounded-xl border border-gray-300 dark:border-gray-700 focus:outline-none focus:ring-4 focus:ring-blue-300/60 dark:focus:ring-blue-900/60 focus:border-blue-400 dark:focus:border-blue-700 bg-white/80 dark:bg-gray-800 shadow-inner transition-all duration-200 ease-in-out text-lg placeholder:text-gray-400 dark:placeholder:text-gray-500"
                        name="password"
                        placeholder="Digite sua senha"
                        onChange={handleChange}
                        autoComplete="current-password"
                        required
                        aria-required="true"
                        aria-describedby="password-error"
                    />
                </div>
                <button
                    type="submit"
                    className="mx-auto block w-2/3 max-w-xs bg-gradient-to-r from-blue-700 via-cyan-400 to-blue-600 dark:from-gray-800 dark:via-cyan-900 dark:to-gray-700 text-white font-extrabold py-3 rounded-xl shadow-lg hover:from-blue-800 hover:to-cyan-500 dark:hover:from-gray-900 dark:hover:to-cyan-800 hover:scale-105 transition-all duration-200 ease-in-out mb-5 focus:outline-none focus:ring-4 focus:ring-cyan-400/60 dark:focus:ring-cyan-900/60 focus:ring-offset-2 active:scale-95"
                disabled={loading}
          style={{ padding: '10px 20px', cursor: loading ? 'not-allowed' : 'pointer' }}>Logar</button>
           {loading ? 'Carregando...' : ''}
                
                
                <a
                    className="block text-center text-base text-blue-700 dark:text-cyan-400 hover:underline hover:text-cyan-500 dark:hover:text-cyan-300 transition duration-200 font-medium"
                    href="/password-reset"
                    aria-label="Redefinir senha"
                >
                    Esqueceu sua senha?
                </a>
            </form>
        </div>
        </>
    );
};

export default Home;