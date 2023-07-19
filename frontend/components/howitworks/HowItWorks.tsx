import styles from './howitworks.module.css';
import Steps from './Steps';

export default function HowItWorks() {
  return <div className={styles['howitworks-container']}>
    <h2>How It Works</h2>

    <div className={styles.row}>
      <Steps title='Step 1' text='testing 123'/>
      <Steps title='Step 2' text='testing 123'/>
    </div>

    <div className={styles.row}>
      <Steps title='Step 3' text='testing 123'/>
      <Steps title='Step 4' text='testing 123'/>
    </div>
  </div>
}