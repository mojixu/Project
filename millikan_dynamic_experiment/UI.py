import streamlit as st
import pandas as pd
import numpy as np

def main():
    if 'num_drops' not in st.session_state:
        st.session_state.num_drops = 3
    if 'page' not in st.session_state:
        st.session_state.page = 'param_input'

    if st.session_state.page == 'param_input':
        parameter_input()
    elif st.session_state.page == 'select_num_drops':
        select_num_drops()
    elif st.session_state.page == 'data_input':
        oil_drop_data_input()
    elif st.session_state.page == 'result_display':
        result_display()
    elif st.session_state.page == 'completion':
        completion_page()

def parameter_input():
    st.title("⚛️ 密立根油滴实验 - 参数输入 ⚛️")
    st.markdown("""
    <div style="
        background-color: #f0f8ff;
        padding: 30px;
        text-align: center;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="color: #1e90ff;">欢迎来到密立根油滴实验！</h2>
        <p style="font-size: 1.2em; color: #000000;">请为实验输入默认参数，让我们一起探索电子的奥秘。</p>
        <div style="margin-top: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Oil_Drop_Experiment_Illustration.svg/1024px-Oil_Drop_Experiment_Illustration.svg.png" alt="Millikan Oil Drop Experiment" style="width: 250px; border-radius: 15px;">
        </div>
    </div>
""", unsafe_allow_html=True)

    with st.form("param_form"):
        rho_oil = st.number_input("油的密度 ρ (kg/m³)", value=981.0)
        g = st.number_input("重力加速度 g (m/s²)", value=9.794,format="%.3f")
        eta = st.number_input("粘滞系数 η (kg/(m·s))", value=1.83e-5, format="%.2e")
        L = st.number_input("匀速上升/下降的距离 L (m)", value=2.00e-3, format="%.3e")
        b = st.number_input("修正系数 b (m·Pa)", value=8.226e-3, format="%.3e")
        p_atm = st.number_input("大气压强 p (Pa)", value=1.013e5, format="%.3e")
        d = st.number_input("平行极板间距 d (m)", value=5.00e-3, format="%.2e")

        submitted = st.form_submit_button("下一步")

        if submitted:
            st.session_state.parameters = {
                'rho_oil': rho_oil, 'g': g, 'eta': eta, 'L': L, 'b': b, 'p_atm': p_atm, 'd': d
            }
            st.session_state.page = 'select_num_drops'
            st.experimental_rerun = True

def select_num_drops():
    st.title("💧密立根油滴实验 - 选择油滴数量💧")
    st.markdown("""
        <div style="
            background-color: #f0f8ff;
            padding: 30px;
            text-align: center;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
        ">
            <h2 style="color: #1e90ff;">请选择您要输入的油滴数量</h2>
            <p style="font-size: 1.2em; color: #000000;">您可以选择任意数量的油滴来进行实验，输入数量后点击下一步。</p>
        </div>
    """, unsafe_allow_html=True)

    num_drops = st.number_input("请输入油滴的数量：", min_value=1, max_value=30, value=3)
    num_times = st.number_input("请输入每颗油滴匀速上升/下降的次数",min_value=1, max_value=10, value=6)
    if st.button("下一步"):
        st.session_state.num_drops = num_drops
        st.session_state.num_times = num_times
        st.session_state.page = 'data_input'
        st.experimental_rerun = True
def oil_drop_data_input():
    st.title("🔬 密立根油滴实验 - 数据输入 🔬")
    st.markdown(f"""
    <div style="
        background-color: #e6f7ff;
        padding: 30px;
        text-align: center;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: #1e90ff;">请输入 {st.session_state.num_drops} 个油滴的测试数据</h3>
        <p style="font-size: 1.2em; color: #000000;">包括上升电压和{st.session_state.num_times}匀速上升与下降时间，让我们继续实验吧！</p>
        <div style="margin-top: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Millikan_apparatus.svg/1024px-Millikan_apparatus.svg.png" alt="Millikan Oil Drop Apparatus" style="width: 250px; border-radius: 15px;">
        </div>
    </div>
""", unsafe_allow_html=True)

    drop_data = []
    for i in range(1, st.session_state.num_drops + 1):
        st.write(f"### 油滴 {i}")
        U_prime = st.number_input(f"输入油滴 {i} 的上升电压 U (V)", key=f"U_prime_{i}")
        t_rise = [
            st.number_input(f"输入油滴 {i} 的第 {j} 次匀速上升时间 (s)", key=f"t_rise_{i}_{j}")
            for j in range(1, st.session_state.num_times+1)
        ]
        t_fall = [
            st.number_input(f"输入油滴 {i} 的第 {j} 次匀速下降时间 (s)", key=f"t_fall_{i}_{j}")
            for j in range(1, st.session_state.num_times+1)
        ]
        drop_data.append({'U_prime': U_prime, 't_rise': t_rise, 't_fall': t_fall})

    st.session_state.drop_data = drop_data

    col1, col2 = st.columns(2)
    if col1.button("返回参数输入"):
        st.session_state.page = 'param_input'
        st.experimental_rerun = True

    if col2.button("计算"):
        st.session_state.page = 'result_display'
        st.experimental_rerun = True

def result_display():
    st.title("📊 密立根油滴实验 - 结果显示 📊")
    st.markdown("""
    <div style="
        background-color: #f9f9f9;
        padding: 30px;
        text-align: center;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="color: #2e8b57;">实验结果</h3>
        <p style="font-size: 1.2em; color: #000000;">以下是您输入的油滴数据的计算结果。让我们看看这些小小油滴给了我们怎样的启示！</p>
        <div style="margin-top: 20px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Electron.svg/1024px-Electron.svg.png" alt="Electron" style="width: 250px; border-radius: 15px;">
        </div>
    </div>
""", unsafe_allow_html=True)

    parameters = st.session_state.parameters
    drop_data = st.session_state.drop_data

    results = []
    for drop in drop_data:
        if drop['U_prime'] == 0 or any(t == 0 for t in drop['t_rise'] + drop['t_fall']):
            # If any of the drop data is missing, append None values for this row
            results.append({
                '上升电压 (v)': None,
                '平均上升时间 (s)': None,
                '平均下降时间 (s)': None,
                '电荷量 q (x10^-19 C)': None,
                'n 计': None,
                'n 整': None,
                'e 测 (x10^-19 C)': None,
                '相对误差 Er (%)': None
            })
        else:
            U_prime = drop['U_prime']
            avg_t_rise = np.mean(drop['t_rise'])
            avg_t_fall = np.mean(drop['t_fall'])

            # Updated q calculation based on the new formula
            r = np.sqrt((9*parameters['eta']*parameters['L'])/(2*parameters['rho_oil']*parameters['g']*avg_t_fall))
            term1 = ((parameters['eta']*parameters['L'] )/ (1 + (parameters['b'] / (parameters['p_atm'] * r)))) ** (3/2)
            term2 = parameters['d'] / U_prime
            term3 = (1 / avg_t_rise) + (1 / avg_t_fall)
            term4 = (1 / avg_t_fall) ** 0.5
            q = (18 * np.pi / np.sqrt(2 * parameters['rho_oil'] * parameters['g'])) * term1 * (term2 * term3 * term4)
            n_cal = q / 1.602e-19
            n_int = round(n_cal)
            e_measured = q / n_int

            results.append({
                '上升电压 (v)': U_prime,
                '平均上升时间 (s)': round(avg_t_rise, 1),
                '平均下降时间 (s)': round(avg_t_fall, 1),
                '电荷量 q (x10^-19 C)': round(q * 1e19, 3),
                'n 计': round(n_cal, 1),
                'n 整': n_int,
                'e 测 (x10^-19 C)': round(e_measured * 1e19, 3),
                '相对误差 Er (%)': round(abs((e_measured - 1.602e-19) / 1.602e-19) * 100, 2)

            })

    df = pd.DataFrame(results)
    st.write(df)

    col1, col2 = st.columns(2)
    if col1.button("接着测量"):
        st.session_state.page = 'data_input'
        st.experimental_rerun = True

    if col2.button("结束"):
        st.session_state.page = 'completion'
        st.experimental_rerun = True

def completion_page():
    st.title("🎉 感谢使用密立根油滴实验交互系统 🎉")
    st.markdown("""
    <div style="
        background-color: #f0f8ff;
        padding: 50px;
        text-align: center;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    ">
        <h2 style="color: #2e8b57;">祝您生活愉快！🌟</h2>
        <p style="font-size: 1.5em; color: #4b0082;">愿您的每一天都充满科学探索的乐趣和无限的惊喜！</p>
        <div style="margin-top: 30px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/3/3e/Millikan_Oil_Drop_Experiment.gif" alt="Millikan Oil Drop Experiment Animation" style="width: 300px; border-radius: 15px; display: block; margin-left: auto; margin-right: auto;">
        </div>
    </div>
""", unsafe_allow_html=True)
    st.balloons()


main()