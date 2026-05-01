import streamlit as st
import plotly.graph_objects as go
import numpy as np #numpy'yi ekledim çünkü lorenz attractor grafiği için daha hızlı ve kolay bir şekilde veri üretmek istedim, for döngüsüyle tek tek hesaplamak yerine numpy arrayleriyle işlemleri yaparak daha verimli bir şekilde grafiği oluşturuyorum, yani performans artışı sağlamak için numpy kullandım

st.set_page_config(page_title="Sena | Chaos Lab V2", page_icon="🦋",layout= "wide") #sayfa düzenini daha çok genişlettim çünkü bir önceki versiyonda lorenz attractor grafiği sağda sıkışık duruyordu, wide olduğu için daha ferah bir görünüm sağladım, kelebeğim daha rahat uçsun diye wide yaptım yani

if 'x0_val' not in st.session_state:
    st.session_state.x0_val = 0.1000
    st.session_state.y0_val = 0.1100
    st.session_state.z0_val = 0.1000

st.title("🦋 Lorenz Encryption Engine V2") #ana başlık
st.write("Welcome to Sena's Chaos Laboratory. System infrastructure is active") #karşılama mesahjım (greeting message)
st.write("""
This application is a 3D encryption laboratory powered by Chaos Theory and the Butterfly Effect. 
Unlike standard algorithms, it utilizes Edward Lorenz's non-linear differential equations to 
transform your messages and data into unpredictable mathematical chaos.
""")
#kendimce what's it for açıklaması

#first girdi için:
st.subheader("1. Message and Security Key") #birinci girdi başlığı
message = st.text_area("Enter the text you want to encrypt or decrypt: ") 
st.write("**Lorenz Initial Values**") #iki yıldız koydum kalın yazı olsun diye
with st.sidebar:
    st.header("🔑 Security Key Settings") #sidebar başlığı
    x0 = st.number_input("X0 Value", value=st.session_state.x0_val, format="%0.4f")
    y0 = st.number_input("Y0 Value", value=st.session_state.y0_val, format="%0.4f")
    z0 = st.number_input("Z0 Value", value=st.session_state.z0_val, format="%0.4f")
    st.divider() #sidebar içinde ayırıcı çizgi
    st.info("Remember: A tiny change in initial values, completely transforms the encryption key. This is the essence of the Butterfly Effect. Choose wisely!") #hatırlatma mesajım

    st.divider()
    st.header("🎨 Visualization Settings")
    color_theme = st.selectbox("Select Color Theme for the 3D Graph:", ["Viridis", "Cividis", "Plasma", "Inferno", "Magma"]) 
    num_steps = st.slider("Chaos Density (Iterations)", 1000, 10000,2500)
    line_width = st.slider("Line Thickness", 1, 5, 2)

if st.sidebar.button("🎲 Randomize Key"):
    st.session_state.x0_val = np.random.uniform(0.1, 5.0)
    st.session_state.y0_val = np.random.uniform(0.1, 5.0)
    st.session_state.z0_val = np.random.uniform(0.1, 5.0)
    st.rerun()

if st.sidebar.button("♻️ Reset to Default"):
    st.session_state.x0_val = 0.1000
    st.session_state.y0_val = 0.1100
    st.session_state.z0_val = 0.1000
    st.rerun()

def lorenz_encrypt_decrypt(text_or_hex, start_x, start_y, start_z, is_decrypt=False):
    sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0
    dt = 0.01
    
    if is_decrypt:
        data_bytes = bytes.fromhex(text_or_hex.strip())
    else:
        data_bytes = text_or_hex.encode('utf-8')
    x, y, z = start_x, start_y, start_z
    
    for i in range(100): ##çok hoşuma giden bir adım. strange attractore ulaşabilmek için 100 adım(iterasyon) attırıyorum. bu sayede başlangıç değerlerine daha az bağımlı bir anahtar üretiyorum yani daha güvenli bir şifreleeme yapmış oluyorum.
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz
        
    result_bytes = bytearray()
    for b in data_bytes:
        dx = sigma * (y - x) * dt
        dy = (x * (rho - z) - y) * dt
        dz = (x * y - beta * z) * dt
        x, y, z = x + dx, y + dy, z + dz
        
        key_byte = int((abs(x) - int(abs(x))) * 256)
        result_bytes.append(b ^ key_byte)
        
    return result_bytes

st.subheader("2. Action Center & 3D Chaos Graphs")
st.write("---") # ayırıcı çizgi

if st.button("🔒 Encrypt Message", use_container_width=True):
    if message:
        encrypted_data = lorenz_encrypt_decrypt(message, x0, y0, z0, is_decrypt=False)
        st.success("Message Encrypted Successfully!")
        st.code(encrypted_data.hex()) 
        st.balloons()
    else:
        st.warning("Please enter a message to encrypt.")

if st.button("🔓 Decrypt Message", use_container_width=True):
    if message:
        try:
            clean_message = message.strip()
            decrypted_data = lorenz_encrypt_decrypt(clean_message, x0, y0, z0, is_decrypt=True)
            final_text = decrypted_data.decode('utf-8')
            st.success("Message Decrypted Successfully!")
            st.code(final_text)
            st.balloons()
        except UnicodeDecodeError:
            st.error("🚨 Crypto Error: Key mismatch (X0, Y0, Z0) or invalid Hex format. Please ensure you pasted the correct code.")
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")
    else:
        st.warning("Please enter the Hex code to decrypt.")

st.write("### 🦋 The Butterfly Effect")
xs, ys, zs = [x0], [y0], [z0]
curr_x, curr_y, curr_z = x0, y0, z0
sigma, rho, beta = 10.0, 28.0, 8.0 / 3.0 #fonk içindekilerle aynı olmak zorunda
dt = 0.01
for _ in range(num_steps):
    dx = sigma * (curr_y - curr_x) * dt
    dy = (curr_x * (rho - curr_z) - curr_y) * dt
    dz = (curr_x * curr_y - beta * curr_z) * dt
    curr_x += dx
    curr_y += dy
    curr_z += dz
    xs.append(curr_x)
    ys.append(curr_y)
    zs.append(curr_z)

fig = go.Figure(data=go.Scatter3d(x=xs, y=ys, z=zs, mode='lines', line=dict(color=zs, colorscale=color_theme, width=line_width)))
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    height=550,
    paper_bgcolor="rgba(0,0,0,0)",
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
    )
)
st.plotly_chart(fig, use_container_width=True)
st.info(f"📊 **Lab Analysis:** The strange attractor reached a maximum vertical peak (Z-axis) of **{max(zs):.2f}** units during this iteration.")