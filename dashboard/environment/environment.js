import React from 'react';
import { XYPlot, XAxis, YAxis, HorizontalGridLines, LineSeries } from 'react-vis';
import { atom, useRecoilValue } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './environment.scss';


export const environmentState = atom({
	key: 'environment',
	default: {
		fetched: false,
		loggingEnabled: undefined,
		logEntries: {
			temperature: [],
			pressure: [],
			humidity: []
		}
	}
});

const Environment = () => {
	useAPIPoll(environmentState, '/environment/logs', 60000 * 10);
	const environment = useRecoilValue(environmentState);

	const latest = ['temperature', 'pressure', 'humidity'].reduce((accumulator, property) => {
		if (environment.logEntries[property].length === 0) {
			accumulator[property] = undefined;
		} else {
			accumulator[property] = environment.logEntries[property][environment.logEntries[property].length - 1][1];
		}
		return accumulator;
	}, {});

	const chartData = ['temperature', 'pressure', 'humidity'].reduce((accumulator, property) => {
		const entries = environment.logEntries[property];
		accumulator[property] = entries.map((entry) => {
			const timestamp = Date.parse(entry[0]);
			return {
				x: timestamp,
				y: entry[1]
			};
		});
		return accumulator;
	}, {});

	return (
		<>
			<div className="panel-heading">Coop Environment</div>
			<div className="panel-block temperature">
				<div>
					Temperature: { latest.temperature }°F
				</div>
				<XYPlot width={300} height={300} yDomain={[-10, 120]}>
					<HorizontalGridLines />
					<LineSeries data={chartData.temperature} />
					<XAxis />
					<YAxis />
				</XYPlot>
			</div>
			<div className="panel-block pressure">
				<div>
					Pressure: { latest.pressure } mb
				</div>
				<XYPlot width={300} height={300} yDomain={[970, 1040]}>
					<HorizontalGridLines />
					<LineSeries data={chartData.pressure} />
					<XAxis />
					<YAxis />
				</XYPlot>
			</div>
			<div className="panel-block memory-percent">
				<div>
					Humidity: { latest.humidity }%
				</div>
				<XYPlot width={300} height={300} yDomain={[0, 100]}>
					<HorizontalGridLines />
					<LineSeries data={chartData.humidity} />
					<XAxis />
					<YAxis />
				</XYPlot>
			</div>
		</>
	);
};

export default Environment;
